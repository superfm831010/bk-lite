package local

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/nats-io/nats.go"
	"log"
	"nats-executor/utils"
	"os/exec"
	"time"
)

func Execute(req ExecuteRequest, instanceId string) ExecuteResponse {
	// Execute the command with timeout
	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(req.ExecuteTimeout)*time.Second)
	defer cancel()

	log.Printf("Executing command: %s with timeout: %d seconds", req.Command, req.ExecuteTimeout)
	cmd := exec.CommandContext(ctx, "sh", "-c", req.Command)
	output, err := cmd.CombinedOutput()
	response := ExecuteResponse{
		Output:     string(output),
		InstanceId: instanceId,
		Success:    err == nil && ctx.Err() != context.DeadlineExceeded,
	}

	if ctx.Err() == context.DeadlineExceeded {
		log.Printf("Command timed out")
	} else if err != nil {
		log.Printf("Command execution error: %v", err)
	} else {
		log.Printf("Command output: %s", output)
	}

	return response

}

func SubscribeLocalExecutor(nc *nats.Conn, instanceId *string) {
	subject := fmt.Sprintf("local.execute.%s", *instanceId)
	log.Printf("Subscribing to subject: %s", subject)
	nc.Subscribe(subject, func(msg *nats.Msg) {
		// 定义一个临时结构来接收请求方格式
		var incoming struct {
			Args   []json.RawMessage      `json:"args"`
			Kwargs map[string]interface{} `json:"kwargs"`
		}

		if err := json.Unmarshal(msg.Data, &incoming); err != nil {
			log.Printf("Error unmarshalling incoming message: %v", err)
			return
		}

		if len(incoming.Args) == 0 {
			log.Printf("No arguments received")
			return
		}
		var localExecuteRequest ExecuteRequest
		if err := json.Unmarshal(incoming.Args[0], &localExecuteRequest); err != nil {
			log.Printf("Error unmarshalling first arg to local.ExecuteRequest: %v", err)
			return
		}

		log.Printf("Received command: %s", localExecuteRequest.Command)
		responseData := Execute(localExecuteRequest, *instanceId)
		log.Printf("Publishing response to subject: local.execute.response")

		responseContent, _ := json.Marshal(responseData)
		if err := msg.Respond(responseContent); err != nil {
			log.Printf("Error publishing response: %v", err)
		}

	})
}

func SubscribeDownloadToLocal(nc *nats.Conn, instanceId *string) {
	subject := fmt.Sprintf("download.local.%s", *instanceId)
	log.Printf("Subscribing to subject: %s", subject)

	nc.Subscribe(subject, func(msg *nats.Msg) {
		var incoming struct {
			Args   []json.RawMessage      `json:"args"`
			Kwargs map[string]interface{} `json:"kwargs"`
		}

		if err := json.Unmarshal(msg.Data, &incoming); err != nil {
			log.Printf("Error unmarshalling incoming message: %v", err)
			return
		}

		if len(incoming.Args) == 0 {
			log.Printf("No arguments received")
			return
		}

		var downloadRequest utils.DownloadFileRequest
		if err := json.Unmarshal(incoming.Args[0], &downloadRequest); err != nil {
			log.Printf("Error unmarshalling first arg to DownloadFileRequest: %v", err)
			return
		}

		log.Printf("Starting download from bucket %s, file %s to local path %s", downloadRequest.BucketName, downloadRequest.FileKey, downloadRequest.TargetPath)

		var resp ExecuteResponse

		err := utils.DownloadFile(downloadRequest, nc)
		if err != nil {
			log.Printf("Download error: %v", err)
			resp = ExecuteResponse{
				Success:    false,
				Output:     fmt.Sprintf("Failed to download file: %v", err),
				InstanceId: *instanceId,
			}

		} else {
			log.Println("Download completed successfully!")
			resp = ExecuteResponse{
				Success:    true,
				Output:     fmt.Sprintf("File successfully downloaded to %s/%s", downloadRequest.TargetPath, downloadRequest.FileName),
				InstanceId: *instanceId,
			}
		}

		responseContent, _ := json.Marshal(resp)
		if err := msg.Respond(responseContent); err != nil {
			log.Printf("Error responding to download request: %v", err)
		}
	})
}

func SubscribeUnzipToLocal(nc *nats.Conn, instanceId *string) {
	subject := fmt.Sprintf("unzip.local.%s", *instanceId)
	log.Printf("Subscribing to subject: %s", subject)

	nc.Subscribe(subject, func(msg *nats.Msg) {
		var incoming struct {
			Args   []json.RawMessage      `json:"args"`
			Kwargs map[string]interface{} `json:"kwargs"`
		}

		if err := json.Unmarshal(msg.Data, &incoming); err != nil {
			log.Printf("Error unmarshalling incoming message: %v", err)
			return
		}

		if len(incoming.Args) == 0 {
			log.Printf("No arguments received")
			return
		}

		var unzipRequest utils.UnzipRequest
		if err := json.Unmarshal(incoming.Args[0], &unzipRequest); err != nil {
			log.Printf("Error unmarshalling first arg to UnzipRequest: %v", err)
			return
		}

		log.Printf("Starting unzip from file %s to local path %s", unzipRequest.ZipPath, unzipRequest.DestDir)

		// 修复调用 UnzipToDir 的参数问题
		parentDir, err := utils.UnzipToDir(unzipRequest)
		if err != nil {
			log.Printf("Unzip error: %v", err)
			resp := ExecuteResponse{
				Output:     fmt.Sprintf("Failed to unzip file: %v", err),
				InstanceId: *instanceId,
				Success:    false,
			}
			responseContent, _ := json.Marshal(resp)
			if err := msg.Respond(responseContent); err != nil {
				log.Printf("Error responding to unzip request: %v", err)
			}
			return
		}

		log.Printf("Unzip completed successfully! Parent directory: %s", parentDir)
		resp := ExecuteResponse{
			Output:     parentDir,
			InstanceId: *instanceId,
			Success:    true,
		}
		responseContent, _ := json.Marshal(resp)
		if err := msg.Respond(responseContent); err != nil {
			log.Printf("Error responding to unzip request: %v", err)
		}
	})
}
