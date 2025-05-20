package utils

import (
	"archive/zip"
	"os"
	"path/filepath"
	"testing"
)

func TestUnzipToDir(t *testing.T) {
	// 准备测试目录
	zipFilePath := filepath.Join(t.TempDir(), "test.zip")
	destDir := filepath.Join(t.TempDir(), "unzipped")

	// 创建一个临时 zip 文件用于测试
	f, err := os.Create(zipFilePath)
	if err != nil {
		t.Fatalf("failed to create test zip file: %v", err)
	}
	defer f.Close()

	// 创建 zip writer
	zipWriter := zip.NewWriter(f)

	// 添加一个文件
	w, err := zipWriter.Create("testdir/hello.txt")
	if err != nil {
		t.Fatalf("failed to create file in zip: %v", err)
	}
	_, err = w.Write([]byte("Hello, world!"))
	if err != nil {
		t.Fatalf("failed to write to file in zip: %v", err)
	}

	zipWriter.Close()

	// 解压
	req := UnzipRequest{
		ZipPath: zipFilePath,
		DestDir: destDir,
	}

	_, err = UnzipToDir(req)
	if err != nil {
		t.Fatalf("UnzipToDir failed: %v", err)
	}

	// 验证解压后的文件存在
	unzippedFile := filepath.Join(destDir, "testdir", "hello.txt")
	if _, err := os.Stat(unzippedFile); os.IsNotExist(err) {
		t.Fatalf("expected file not found after unzip: %s", unzippedFile)
	}
}
