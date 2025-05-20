package local

type ExecuteRequest struct {
	Command        string `json:"command"`
	ExecuteTimeout int    `json:"execute_timeout"`
}

type ExecuteResponse struct {
	Output     string `json:"result"`
	InstanceId string `json:"instance_id"`
	Success    bool   `json:"success"`
}
