package main

import (
	"crypto/tls"
	"crypto/x509"
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

	// TLS 配置
	TLSEnabled    bool   `yaml:"tls_enabled"`
	TLSHostname   string `yaml:"tls_hostname"`
	TLSCAFile     string `yaml:"tls_ca_file"`
	TLSCertFile   string `yaml:"tls_cert_file"`
	TLSKeyFile    string `yaml:"tls_key_file"`
	TLSSkipVerify bool   `yaml:"tls_skip_verify"`
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

	//log.Printf("Connecting to NATS server at %s", cfg.NATSUrls)
	opts := []nats.Option{
		nats.Name("nats-executor"),
		nats.Compression(true),
		nats.Timeout(time.Duration(cfg.NatsConnTimeout) * time.Second),
	}

	// 添加 TLS 配置
	if cfg.TLSEnabled {
		tlsConfig := &tls.Config{
			InsecureSkipVerify: cfg.TLSSkipVerify,
		}

		// 如果指定了 hostname，设置 ServerName
		if cfg.TLSHostname != "" {
			tlsConfig.ServerName = cfg.TLSHostname
		}

		// 如果提供了证书文件，加载客户端证书
		if cfg.TLSCertFile != "" && cfg.TLSKeyFile != "" {
			cert, err := tls.LoadX509KeyPair(cfg.TLSCertFile, cfg.TLSKeyFile)
			if err != nil {
				log.Fatalf("Failed to load client certificate: %v", err)
			}
			tlsConfig.Certificates = []tls.Certificate{cert}
		}

		// 如果提供了 CA 证书文件，加载 CA 证书
		if cfg.TLSCAFile != "" {
			caCert, err := os.ReadFile(cfg.TLSCAFile)
			if err != nil {
				log.Fatalf("Failed to read CA certificate file: %v", err)
			}
			caCertPool := x509.NewCertPool()
			if !caCertPool.AppendCertsFromPEM(caCert) {
				log.Fatalf("Failed to append CA certificate")
			}
			tlsConfig.RootCAs = caCertPool
		}

		// 添加 TLS 选项到连接选项中
		opts = append(opts, nats.Secure(tlsConfig))
		log.Println("TLS enabled for NATS connection")
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
