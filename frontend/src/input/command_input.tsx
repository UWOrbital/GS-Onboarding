import { useState, useEffect } from "react";
import { CommandResponse, MainCommandResponse } from "../data/response"
import "./command_input.css"
import { createCommand } from "./input_api";

interface CommandInputProp {
  setCommands: React.Dispatch<React.SetStateAction<CommandResponse[]>>
}

const CommandInput = ({ setCommands }: CommandInputProp) => {
  const [selectedCommand, setSelectedCommand] = useState<MainCommandResponse | null>(null);
  const [parameters, setParameters] = useState<{ [key: string]: string }>({});
  // TODO: (Member) Setup anymore states if necessary
  const [mainCommands, setMainCommands] = useState<MainCommandResponse[]>([]);
  const [error, setError] = useState<string | null>(null);

  // TODO: (Member) Fetch MainCommands in a useEffect
  useEffect(() => {
    const fetchMainCommands = async () => {
      try {
        const response = await fetch('http://localhost:8000/main_commands/');
        const data = await response.json();
        setMainCommands(data.data);
      }
      catch(error) {
        setError("Failed to fetch main commands");
        console.error("Error fetching main commands:", error);
     }
    };
    fetchMainCommands();
  }, []);

  const handleParameterChange = (param: string, value: string): void => {
    setParameters((prev) => ({
      ...prev,
      [param]: value,
    }));
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCommand) {
        setError("Please select a command");
        return;
    }

    try {
        const commandParams = Object.values(parameters).join(",");
        const response = await createCommand({
        command_type: selectedCommand.id,
        params: commandParams || null
        });
        
        setCommands(prev => [...prev, response.data]);
        setParameters({}); // Reset parameters after successful submission
        setError(null);
    } catch (error) {
        setError("Failed to create command");
        console.error("Error creating command:", error);
    }
  };

  return (
    <>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select
              value={selectedCommand ? selectedCommand.id : ""}
              onChange={(e) => {
                const selected = mainCommands.find(cmd => cmd.id === parseInt(e.target.value));
                setSelectedCommand(selected || null);
                setParameters({}); // Reset parameters when command changes
              }}
            >
              <option value="" disabled>Select a command</option>
              {mainCommands.map(cmd => (
                <option key={cmd.id} value={cmd.id}>
                  {cmd.name}
                </option>
              ))}
            </select>
          </div>
          {selectedCommand?.params?.split(",").map((param) => (
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
    </>
  )
}

export default CommandInput;
