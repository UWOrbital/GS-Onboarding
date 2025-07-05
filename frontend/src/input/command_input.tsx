import { useEffect, useState } from "react";
import { MainCommandResponse } from "../data/response";
import "./command_input.css";
import { createCommand, getMainCommands } from "./input_api";
import { CommandRequest } from "../data/request";

const CommandInput = () => {
  // TODO: (Member) Setup state and useEffect calls here
  const [mainCommands, setMainCommands] = useState<MainCommandResponse[]>([]);

  const [selectedCommandId, setSelectedCommandId] = useState<string | null>(null);
  const [commandParams, setCommandParams] = useState<string | null>(null);

  useEffect(() => {
    const getMainCommandsFn = async () => {
      try {
        const data = await getMainCommands();
        setMainCommands(data.data);
        setSelectedCommandId(data.data[0].id.toString());
      } catch (error) {
        alert("Failed to retrieve main commands")
      }
      
    };

    getMainCommandsFn();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedCommandId) {
      alert(`Select a command with an existing ID before submitting`)
      return;
    }

    const command: CommandRequest = {
      command_type: selectedCommandId,
      params: commandParams,
    };

    createCommand(command);
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select onChange={(e) => setSelectedCommandId(e.target.value)}>
              {/* TODO: (Member) Display the list of commands based on the get commands request*/}
              {mainCommands.map((command, index) => (
                <option key={index} value={command.id}>
                  {command.name}
                </option>
              ))}
            </select>
          </div>
          <input onChange={(e) => setCommandParams(e.target.value)} />{" "}
          {/* TODO: (Member) Add input handling here if the selected command has a param input*/}
          <button type="submit">Submit</button>
        </div>
      </form>
    </>
  );
};

export default CommandInput;
