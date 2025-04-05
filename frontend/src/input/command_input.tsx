import "./command_input.css";
import { useState, useEffect } from "react";
import { getCommands, createCommand } from "../display/command_api";
import { CommandResponse } from "../data/response";

const CommandInput = () => {
  // TODO: (Member) Setup state and useEffect calls here
  const [commands, setCommands] = useState<CommandResponse[]>([]);
  const [selectedCommand, setSelectedCommand] = useState<string>("");
  const [params, setParams] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null); // Error state for feedback

  useEffect(() => {
    const fetchCommands = async () => {
      try {
        const data = await getCommands();
        setCommands(data.data); // Set the main commands
      } catch (error) {
        console.error("Error fetching commands:", error);
        setError("Failed to fetch commands. Please try again later.");
      }
    };

    fetchCommands();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    // TODO:(Member) Submit to your post endpoint
    e.preventDefault(); //prevent page refresh for default page submission
    
    if (!selectedCommand) {
      setError("Please select a command!");
      return; 
    }

    try {
      const concatenatedParams = params.join(", ");
      const response = await createCommand(selectedCommand, concatenatedParams);
      console.log("Command created successfully:", response);
  
      // Reset form state
      setSelectedCommand("");
      setParams([]);
      setError(null); // Clear any previous errors

      window.location.reload(); // Reload the page to reflect changes
  
    } catch (error) {
      console.error("Failed to create command:", error);
      setError("Failed to create command. Please try again.");
    }
  };

  const handleParamChange = (index: number, value: string) => {
    const newParams = [...params];
    newParams[index] = value;
    setParams(newParams);
  };

  const selectedCommandDetails = commands.find(command => command.id.toString() === selectedCommand);

  return (
    <>
      <form>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select onChange={(e) => setSelectedCommand(e.target.value)} value={selectedCommand}>{/* TODO: (Member) Display the list of commands based on the get commands request*/}
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

          {/* Render input fields dynamically based on the selected command's parameters */}
          {selectedCommandDetails && selectedCommandDetails.params && selectedCommandDetails.params !== "null" && (
            <div>
              {/* Convert params string into an array and handle them */}
              {selectedCommandDetails.params.split(",").map((param, index) => (
                <div key={index}>
                  <label>{param}</label>
                  <input 
                    type="text"
                    placeholder={`Enter ${param}`}
                    value={params[index] || ''}
                    onChange={(e) => handleParamChange(index, e.target.value)}
                  /> {/* TODO: (Member) Add input handling here if the selected command has a param input*/}
                </div>
              ))}
            </div>
          )}

          {/* Error Message */}
          {error && <div className="error">{error}</div>} 

          <button type="submit" onClick={handleSubmit}>Submit</button>
        </div>
      </form>
    </>
  )
}

export default CommandInput;
