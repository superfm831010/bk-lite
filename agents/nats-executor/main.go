package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/nats-io/nats.go"
	"gopkg.in/yaml.v3"

	"nats-executor/local"
	"nats-executor/ssh"
)

type Config struct {
	NATSUrls        string `yaml:"nats_urls"`
	NATSInstanceID  string `yaml:"nats_instanceId"`
	NatsConnTimeout int    `yaml:"nats_conn_timeout"`
}

func loadConfig(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}
	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("failed to parse config file: %w", err)
	}
	return &cfg, nil
}

func main() {
	configPath := flag.String("config", "", "Path to the config file (YAML format)")
	flag.Parse()

	if *configPath == "" {
		log.Fatal("Please specify the config file path using --config")
	}

	cfg, err := loadConfig(*configPath)
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)

	}

	log.Printf("Connecting to NATS server at %s", cfg.NATSUrls)
	opts := []nats.Option{
		nats.Name("nats-executor"),
		nats.Compression(true),
		nats.Timeout(time.Duration(cfg.NatsConnTimeout) * time.Second),
	}

	nc, err := nats.Connect(cfg.NATSUrls, opts...)
	if err != nil {
		log.Fatalf("Failed to connect to NATS server: %v", err)
	}
	defer nc.Close()
	log.Println("Connected to NATS server")

	// 注册各类订阅
	local.SubscribeLocalExecutor(nc, &cfg.NATSInstanceID)
	local.SubscribeDownloadToLocal(nc, &cfg.NATSInstanceID)
	local.SubscribeUnzipToLocal(nc, &cfg.NATSInstanceID)

	ssh.SubscribeSSHExecutor(nc, &cfg.NATSInstanceID)
	ssh.SubscribeDownloadToRemote(nc, &cfg.NATSInstanceID)
	ssh.SubscribeUploadToRemote(nc, &cfg.NATSInstanceID)

	log.Println("Waiting for messages...")
	select {}
}
