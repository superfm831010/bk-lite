package ssh

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/melbahja/goph"
	"github.com/nats-io/nats.go"
	"golang.org/x/crypto/ssh"
	"log"
	"nats-executor/local"
	"nats-executor/utils"
	"time"
)

func Execute(req ExecuteRequest, instanceId string) ExecuteResponse {
	auth := goph.Password(req.Password)
	client, err := goph.NewConn(&goph.Config{
		User:     req.User,
		Addr:     req.Host,
		Port:     req.Port,
		Auth:     auth,
		Timeout:  30 * time.Second,
		Callback: ssh.InsecureIgnoreHostKey(), // 👈 跳过 known_hosts 验证
	})

	if err != nil {
		log.Printf("Failed to create new SSH client: %v", err)
		return ExecuteResponse{
			InstanceId: instanceId,
			Success:    false,
			Output:     fmt.Sprintf("Failed to create new SSH client: %v", err),
		}
	}

	defer client.Close()

	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(req.ExecuteTimeout)*time.Second)
	defer cancel()

	out, err := client.RunContext(ctx, req.Command)
	if err != nil {
		if ctx.Err() == context.DeadlineExceeded {
			log.Printf("Command timed out")
		} else {
			log.Printf("Command execution error: %v", err)
		}
		return ExecuteResponse{
			Output:     string(out),
			InstanceId: instanceId,
			Success:    false,
		}
	}

	return ExecuteResponse{
		Output:     string(out),
		InstanceId: instanceId,
		Success:    true,
	}
}

func SubscribeSSHExecutor(nc *nats.Conn, instanceId *string) {
	subject := fmt.Sprintf("ssh.execute.%s", *instanceId)
	log.Printf("Subscribing to subject: %s", subject)
	nc.Subscribe(subject, func(msg *nats.Msg) {
		// 解析 request 的标准结构
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

		var sshExecuteRequest ExecuteRequest
		if err := json.Unmarshal(incoming.Args[0], &sshExecuteRequest); err != nil {
			log.Printf("Error unmarshalling first arg to ssh.ExecuteRequest: %v", err)
			return
		}

		log.Printf("Received SSH command: %s", sshExecuteRequest.Command)
		responseData := Execute(sshExecuteRequest, *instanceId)
		log.Printf("Publishing SSH response using msg.Respond")

		responseContent, _ := json.Marshal(responseData)
		if err := msg.Respond(responseContent); err != nil {
			log.Printf("Error responding to SSH request: %v", err)
		}
	})
}

func SubscribeDownloadToRemote(nc *nats.Conn, instanceId *string) {
	subject := fmt.Sprintf("download.remote.%s", *instanceId)
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

		var downloadRequest DownloadFileRequest

		if err := json.Unmarshal(incoming.Args[0], &downloadRequest); err != nil {
			log.Printf("Error unmarshalling first arg to DownloadFileRequest: %v", err)
			return
		}

		log.Printf("Starting download from bucket %s, file %s to local path %s", downloadRequest.BucketName, downloadRequest.FileKey, downloadRequest.TargetPath)

		// 下载文件到本地
		localdownloadRequest := utils.DownloadFileRequest{
			BucketName:     downloadRequest.BucketName,
			FileKey:        downloadRequest.FileKey,
			FileName:       downloadRequest.FileName,
			TargetPath:     downloadRequest.TargetPath,
			ExecuteTimeout: downloadRequest.ExecuteTimeout,
		}

		err := utils.DownloadFile(localdownloadRequest, nc)
		if err != nil {
			log.Printf("Error downloading file: %v", err)
			return
		}

		// 使用sshpass处理带密码的scp传输
		scpCommand := fmt.Sprintf("sshpass -p '%s' scp -o StrictHostKeyChecking=no -P %d -r %s/%s %s@%s:%s",
			downloadRequest.Password,
			downloadRequest.Port,
			localdownloadRequest.TargetPath,
			localdownloadRequest.FileName,
			downloadRequest.User,
			downloadRequest.Host,
			downloadRequest.TargetPath)

		localExecuteRequest := local.ExecuteRequest{
			Command:        scpCommand,
			ExecuteTimeout: downloadRequest.ExecuteTimeout,
		}

		log.Printf("Starting file transfer to remote host: %s@%s:%s", downloadRequest.User, downloadRequest.Host, downloadRequest.TargetPath)
		responseData := local.Execute(localExecuteRequest, *instanceId)

		responseContent, _ := json.Marshal(responseData)
		if err := msg.Respond(responseContent); err != nil {
			log.Printf("Error responding to download request: %v", err)
		}
	})
}

func SubscribeUploadToRemote(nc *nats.Conn, instanceId *string) {
	subject := fmt.Sprintf("upload.remote.%s", *instanceId)
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

		var uploadRequest UploadFileRequest

		if err := json.Unmarshal(incoming.Args[0], &uploadRequest); err != nil {
			log.Printf("Error unmarshalling first arg to UploadFileRequest: %v", err)
			return
		}

		log.Printf("Starting upload from local path %s to remote host %s@%s:%s", uploadRequest.SourcePath, uploadRequest.User, uploadRequest.Host, uploadRequest.TargetPath)

		// 使用sshpass处理带密码的scp传输
		scpCommand := fmt.Sprintf("sshpass -p '%s' scp -o StrictHostKeyChecking=no -P %d -r %s %s@%s:%s",
			uploadRequest.Password,
			uploadRequest.Port,
			uploadRequest.SourcePath,
			uploadRequest.User,
			uploadRequest.Host,
			uploadRequest.TargetPath)

		localExecuteRequest := local.ExecuteRequest{
			Command:        scpCommand,
			ExecuteTimeout: uploadRequest.ExecuteTimeout,
		}

		log.Printf("Executing SCP command to upload file")
		responseData := local.Execute(localExecuteRequest, *instanceId)

		responseContent, _ := json.Marshal(responseData)
		if err := msg.Respond(responseContent); err != nil {
			log.Printf("Error responding to upload request: %v", err)
		}
	})
}
