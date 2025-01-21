import { useState, useEffect } from "react";
import "./command_input.css";
import { getMainCommands, createCommand } from "./input_api"; // Assuming these are your API functions
import {
  MainCommandListResponse,
  MainCommandResponse,
} from "../data/response"; 

const CommandInput = () => {
  const [commands, setCommands] = useState<MainCommandResponse[]>([]); 
  const [selectedCommand, setSelectedCommand] = useState<MainCommandResponse | null>(null);
  const [parameters, setParameters] = useState<{ [key: string]: string }>({});

  // fetch main commands 
  useEffect(() => {
    const fetchCommands = async () => {
      try {
        const response: MainCommandListResponse = await getMainCommands();
        setCommands(response.data); 
      } catch (error) {
        alert(`Failed to fetch commands: ${error}`);
      }
    };
    fetchCommands();
  }, []);

  // handlers 
  const handleParameterChange = (paramName: string, value: string) => {
    setParameters((prev) => ({
      ...prev,
      [paramName]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
  
    if (!selectedCommand) {
      alert("No command selected.");
      return;
    }
  
    // check if all required parameters are provided
    const requiredParams = selectedCommand.params?.split(",") || [];
    for (const param of requiredParams) {
      if (!parameters[param]) {
        alert(`Missing value for required parameter: ${param}`);
        return;
      }
    }
  
    const paramsCSV = requiredParams.map((param) => parameters[param]).join(",");
  
    try {
      const requestData = {
        command_type: selectedCommand.id,
        params: paramsCSV,
        name: selectedCommand.name,
        format: "csv", 
      };

      const response = await createCommand(requestData);
      console.log("Command submitted successfully:", response);
      setSelectedCommand(null);
      setParameters({}); 
    } catch (error) {
      alert(`Failed to submit command: ${error}`);
    }
    // this is me being extremely lazy but it works
    window.location.reload();
  };
  
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div> 
            {/* command selection */}
            <label >Command Type: </label>
            <select
              value={selectedCommand?.id || ""} 
              onChange={(e) => setSelectedCommand( commands.find((cmd) => cmd.id === parseInt(e.target.value)) || null)}>
              <option value="" disabled>
                Select a command
              </option>
              {commands.map((cmd) => (
                <option key={cmd.id} value={cmd.id}>
                  {cmd.name}
                </option>
              ))}
            </select>
          </div>
          {/* Parameter input */}
          {selectedCommand &&
            selectedCommand.params &&
            selectedCommand.params.split(",").map((param) => (
              <div key={param}>
                <label htmlFor={`param-${param}`}>{param}: </label>
                <input
                  id={`param-${param}`}
                  type="text"
                  value={parameters[param] || ""}
                  onChange={(e) => handleParameterChange(param, e.target.value)}
                  placeholder={`Enter ${param}`}
                />
              </div>
            ))}
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
};

export default CommandInput;
