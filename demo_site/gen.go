package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func allStlFiles(dir string) []string {
	var paths []string
	filepath.Walk(dir, func(path string, f os.FileInfo, err error) error {
		if filepath.Ext(path) == ".stl" {
			paths = append(paths, path)
		}
		return nil
	})
	return paths
}

func main() {
	inputFilepathFlag := flag.String("input_dir", "", "Directory to pull stls from")
	// outputDirFlag := flag.String("output_dir", "", "Directory to write site to")
	flag.Parse()

	if *inputFilepathFlag == "" {
		fmt.Fprintln(os.Stderr, "Please provide an input directory")
		flag.Usage()
		os.Exit(1)
	}

	if !strings.HasSuffix(*inputFilepathFlag, "/") {
		*inputFilepathFlag += "/"
	}

	for _, p := range allStlFiles(*inputFilepathFlag) {
		fmt.Printf("Found stl: %s\n", p)
	}
}
