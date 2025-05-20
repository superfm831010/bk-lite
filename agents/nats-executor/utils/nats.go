package utils

import (
	"context"
	"fmt"
	"github.com/nats-io/nats.go"
	"log"
	"nats-executor/jetstream"
	"time"
)

type DownloadFileRequest struct {
	BucketName     string `json:"bucket_name"`
	FileKey        string `json:"file_key"`
	FileName       string `json:"file_name"`
	TargetPath     string `json:"target_path"`
	ExecuteTimeout int    `json:"execute_timeout"`
}

func DownloadFile(req DownloadFileRequest, nc *nats.Conn) error {
	// 设置超时管理
	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(req.ExecuteTimeout)*time.Second)
	defer cancel()

	log.Printf("Starting download with file_key: %s, target_path: %s, file_name: %s, timeout: %d seconds", req.FileKey, req.TargetPath, req.FileName, req.ExecuteTimeout)

	// 创建 JetStream 客户端
	client, err := jetstream.NewJetStreamClient(nc, req.BucketName)
	if err != nil {
		return fmt.Errorf("failed to create JetStream client: %w", err)
	}

	// 执行下载操作
	if err := client.DownloadToFile(req.FileKey, req.TargetPath, req.FileName); err != nil {
		return fmt.Errorf("failed to download file: %w", err)
	}

	// 检查是否超时（注意：timeout 会在 ctx.Done() 被触发时出现）
	if ctx.Err() == context.DeadlineExceeded {
		return fmt.Errorf("download operation timed out")
	}

	log.Println("Download completed successfully!")
	return nil
}
