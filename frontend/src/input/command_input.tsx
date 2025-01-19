import { useState } from "react";
import "./command_input.css"
const CommandInput = () => {
  // TODO: (Member) Setup state and useEffect calls here
  const { command, setCommand } = useState("");

  const handleSubmit = () => {
    // TODO:(Member) Submit to your post endpoint 
  }
  
  return (
    <>
      <form>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select>{/* TODO: (Member) Display the list of commands based on the get commands request*/}
              <option value={"1"}>Command 1</option>
              <option value={"2"}>Command 2</option>
              <option value={"3"}>Command 3</option>
            </select>
          </div>
          <input /> {/* TODO: (Member) Add input handling here if the selected command has a param input*/}
          <button onClick={handleSubmit}>Submit</button>
        </div>
      </form>
    </>
  )
}

export default CommandInput;
