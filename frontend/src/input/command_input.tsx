import "./command_input.css"
import { useState, useEffect } from "react";
import { getCommands, createCommand } from "../display/command_api";
import { CommandResponse } from "../data/response";

const CommandInput = () => {
  // TODO: (Member) Setup state and useEffect calls here
  const [commands, setCommands] = useState<CommandResponse[]>([]); 
  const [selectedCommand, setSelectedCommand] = useState<string>(""); 
  const [params, setParams] = useState<string>(""); 

  useEffect(() => {
    const fetchCommands = async () => {
      try {
        const data = await getCommands();
        console.log("Fetched commands:", data);
        setCommands(data.data);
      } catch (error) {
        console.error("Error fetching commands:", error);
      }
    };

    fetchCommands();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    // TODO:(Member) Submit to your post endpoint
    e.preventDefault(); //prevent page refresh

    if (!selectedCommand) {
      alert("Please select a command!");
      return; 
  }

  try {
    const response = await createCommand(selectedCommand, params);
    console.log("Command created successfully:", response);

    setSelectedCommand("");
    setParams("");

    const updatedData = await getCommands();
    setCommands(updatedData.data);
    } catch (error) {
      console.error("Failed to create command:", error);
    }
  };
  

  return (
    <>
      <form>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select onChange={(e) => setSelectedCommand(e.target.value)}>{/* TODO: (Member) Display the list of commands based on the get commands request*/}
              <option value="">Select a command</option>
              {commands.length > 0 ? (
                commands.map((command) => (
                  <option key={command.id} value={command.id.toString()}>
                    {command.command_type}
                  </option>
                ))
              ) : (
                <option disabled>No commands available</option>
              )}
            </select>
          </div>
          <input 
            type="text"
            placeholder="Enter parameters (if required)"
            value={params}
            onChange={(e) => setParams(e.target.value)} 
            /> {/* TODO: (Member) Add input handling here if the selected command has a param input*/}
          <button onClick={handleSubmit}>Submit</button>
        </div>
      </form>
    </>
  )
}

export default CommandInput;
