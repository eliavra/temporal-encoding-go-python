package protobug

import (
	"time"

	bug "github.com/temporalio/proto-bug/protobug/bug"
	"go.temporal.io/sdk/workflow"
)

func Workflow(ctx workflow.Context, name string) (string, error) {
	ao := workflow.ActivityOptions{
		StartToCloseTimeout: 10 * time.Second,
	}
	ctx = workflow.WithActivityOptions(ctx, ao)

	logger := workflow.GetLogger(ctx)
	logger.Info("protobug workflow started", "name", name)

	var result bug.HelloResponse
	req := &bug.HelloRequest{Name: name}
	err := workflow.ExecuteActivity(ctx, "print_prto", &req).Get(ctx, &result)
	if err != nil {
		logger.Error("Activity failed.", "Error", err)
		return "", err
	}

	logger.Info("protobug workflow completed.", "result.Message", result.Message)
	return result.Message, nil
}
