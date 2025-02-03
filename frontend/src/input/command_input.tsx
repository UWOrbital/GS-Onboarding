import "./command_input.css"
import { useState, useEffect } from "react"
import { MainCommandResponse } from "../data/response"
import { createCommand, getMainCommands } from "./input_api"


const CommandInput = () => {
  // TODO: (Member) Setup state and useEffect calls here
  const [mainCommands, setMainCommands] = useState<MainCommandResponse[]>([])
  const [commandType, setCommandType] = useState<MainCommandResponse>({id: 0, name: "", params: null, format: null, data_size: 0, total_size: 0})
  const [params, setParams] = useState<Map<string, string>>(new Map());
  
  useEffect(() => {
    const setMainCommandsFn = async () => {
      const data = await getMainCommands()
      if(data.data.length == 0) {
        alert("Error occured. Please try again later.")
        return
      }
      setMainCommands(data.data)
      setCommandType(data.data[0])

      const parameters = data.data[0].params?.split(",") || []
      let paramsObject : Map<string, string> = new Map()
    
      for(const param of parameters) {
        paramsObject.set(param, "")
      }
      setParams(paramsObject);
    }
    setMainCommandsFn();
  }, [])


  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    // TODO:(Member) Submit to your post endpoint    
    e.preventDefault();

    //Check if parameters are valid
    const allParams = commandType?.params?.split(",") || [];
    const paramsList = []

    const missingParams = []
    for (const param of allParams) {
      if (!params.get(param)) {
        missingParams.push(param)
      }
      paramsList.push(params.get(param))
    }
    if(missingParams.length != 0) {
      alert(`Parameters missing: ${missingParams.join(", ")}`)
      return;
    }
    

    const reqBody = {
      command_type: commandType?.id || 0,
      params: paramsList.join(",")
    };

    
    const createCommandFn = async () => {
      await createCommand(reqBody);
      window.location.reload();
    }
    createCommandFn();
  }

  const changeCommandType = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const type : MainCommandResponse = mainCommands.find(cmd => cmd.id == +e.target.value) || {id: 0, name: "", params: null, format: null, data_size: 0, total_size: 0}
    setCommandType(type)
    const parameters = type?.params?.split(",") || []
    let paramsObject : Map<string, string> = new Map()
    for(const param of parameters) {
      paramsObject.set(param, "")
    }
    setParams(paramsObject)
  }

  const changeParam = (e: React.ChangeEvent<HTMLInputElement>) => {
    const param = e.target.id
    const value = e.target.value

    setParams(prevParams => {
      const newParams = new Map(prevParams);
      newParams.set(param, value);
      return newParams;
    })
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            {/* TODO: (Member) Display the list of commands based on the get commands request*/}
            <select 
              value={commandType.id} 
              onChange={changeCommandType}>
              {mainCommands.map(cmd => (<option value={cmd.id}>{cmd.name}</option>))}
            </select>
          </div>
        
           {/* TODO: (Member) Add input handling here if the selected command has a param input*/}
          {commandType && 
            commandType.params?.split(",").map((param) => (<input value={params.get(param)} id={param} placeholder={`Enter ${param}`} onChange={changeParam}/>))}
            
          <button type="submit">Submit</button>
        </div>
      </form>
    </> 
  )
}

export default CommandInput;