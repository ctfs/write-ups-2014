package log

import (
	"log"
	"os"
)

type Logger struct {
	*log.Logger
	verbose bool
}

func New() *Logger {
	return &Logger{
		log.New(os.Stderr, "", log.LstdFlags),
		false,
	}
}

var std = New()

// Our own methods

func Verbose() bool {
	return std.verbose
}

func SetVerbose(verbose bool) {
	std.verbose = verbose
}

func Debugln(msg string) {
	if std.verbose {
		std.Println(msg)
	}
}

func Debugf(format string, v ...interface{}) {
	if std.verbose {
		std.Printf(format, v...)
	}
}

// These methods are borrowed from the standard library's "log"

func Flags() int {
	return std.Flags()
}

func SetFlags(flag int) {
	std.SetFlags(flag)
}

func Prefix() string {
	return std.Prefix()
}

func SetPrefix(prefix string) {
	std.SetPrefix(prefix)
}

func Print(v ...interface{}) {
	std.Print(v...)
}

func Printf(format string, v ...interface{}) {
	std.Printf(format, v...)
}

func Println(v ...interface{}) {
	std.Println(v...)
}

func Fatal(v ...interface{}) {
	std.Fatal(v...)
}

func Fatalf(format string, v ...interface{}) {
	std.Fatalf(format, v...)
}

func Fatalln(v ...interface{}) {
	std.Fatalln(v...)
}

func Panic(v ...interface{}) {
	std.Panic(v...)
}

func Panicf(format string, v ...interface{}) {
	std.Panicf(format, v...)
}

func Panicln(v ...interface{}) {
	std.Panicln(v...)
}
