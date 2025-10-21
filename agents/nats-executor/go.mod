module nats-executor

go 1.18

require (
	github.com/melbahja/goph v1.4.0
	github.com/nats-io/nats.go v1.46.1
	golang.org/x/crypto v0.43.0
	gopkg.in/yaml.v3 v3.0.1
)

require (
	github.com/klauspost/compress v1.18.0 // indirect
	github.com/kr/fs v0.1.0 // indirect
	github.com/nats-io/nkeys v0.4.11 // indirect
	github.com/nats-io/nuid v1.0.1 // indirect
	github.com/pkg/errors v0.9.1 // indirect
	github.com/pkg/sftp v1.13.5 // indirect
	golang.org/x/sys v0.37.0 // indirect
)

// Replace dependencies requiring Go 1.24+ with Go 1.23 compatible versions
replace (
	golang.org/x/crypto v0.43.0 => golang.org/x/crypto v0.27.0
	golang.org/x/sys v0.37.0 => golang.org/x/sys v0.26.0
)
