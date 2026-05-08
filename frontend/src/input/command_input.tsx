import { useEffect, useState } from "react";
import { CommandResponse, MainCommandResponse } from "../data/response"
import { createCommand, getMainCommands } from "./input_api";
import "./command_input.css"

interface CommandInputProp {
  setCommands: React.Dispatch<React.SetStateAction<CommandResponse[]>>
}

const CommandInput = ({ setCommands }: CommandInputProp) => {
  const [selectedCommand, setSelectedCommand] = useState<MainCommandResponse | null>(null);
  const [parameters, setParameters] = useState<{ [key: string]: string }>({});
  const [Command, setCommand] = useState<MainCommandResponse[]>([])

  useEffect(() => {
    const fetchCommand = async () => {
      try {
            const data = await getMainCommands();
            setCommand(data.data);
          } catch (error) {
            console.error(`Error fetching commands: ${error}`);
          }
    }; 
    fetchCommand()
  }, [])


  const handleParameterChange = (param: string, value: string): void => {
    setParameters((prev) => ({
      ...prev,
      [param]: value,
    }));
  }

  const handleSubmit = async (e: React.FormEvent) => {
  
    e.preventDefault();
    if (!selectedCommand){
      return;
    }
    try {
      const params = Object.values(parameters).join(",");
      const data = await createCommand({
        command_type: selectedCommand.id,
        params: params,
      });

      setCommands((prev) => [...prev, data.data]);

    } catch (error) {
      console.error(`Error creating command: ${error}`);
    }

  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select
              value = {selectedCommand?.id ?? ""}
              onChange={(e) => {
                  const command = Command.find((cmd) => cmd.id === Number(e.target.value));
                  setSelectedCommand(command ?? null);
                  setParameters({});
              }}
              > 
              <option value = "">Select a command</option>    
              
              {Command.map((command) => (
                <option key={command.id} value={command.id}>{command.name}</option>
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
