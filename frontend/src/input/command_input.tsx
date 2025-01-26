import "./command_input.css"
import { useState, useEffect } from "react"
import { MainCommandResponse } from "../data/response"
import { createCommand, getMainCommands } from "./input_api"


const CommandInput = () => {
  // TODO: (Member) Setup state and useEffect calls here
  const [mainCommands, setMainCommands] = useState<MainCommandResponse[]>([])
  const [commandType, setCommandType] = useState<MainCommandResponse | null>(null)
  const [params, setParams] = useState<{[key: string] : string}>({})
  
  useEffect(() => {
    const setMainCommandsFn = async () => {
      const data = await getMainCommands()
      setMainCommands(data.data)

      setCommandType(data.data[0])

      const parameters = commandType?.params?.split(",") || []
      let paramsObject : { [key: string]: string } = {}
      for(const param of parameters) {
        paramsObject[param] = ""
      }
      setParams(paramsObject);
    }
    setMainCommandsFn();
  }, [])
  

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    // TODO:(Member) Submit to your post endpoint    
    e.preventDefault();

    //check if parameters are valid
    const allParams = commandType?.params?.split(",") || [];
    const paramsList = []
    for (const param of allParams) {
      if (!params[param]) {
        alert("Parameter missing")
        return;
      }
      paramsList.push(params[param])
    }
    

    const reqBody = {
      command_type: commandType?.id || 0,
      params: paramsList.join(",")
    };

    //console.log('Req body:', reqBody);

    
    const createCommandFn = async () => {
      await createCommand(reqBody);
      window.location.reload();
    }
    createCommandFn();
  }

  /*
          <input value={params} onChange={(e) => setParams(e.target.value)}/>
          {// Use parameters of command type to output input boxes}
          { .params.map(param => (<input id={} value={}>{cmd.name}</option>))}
  */
  //console.log(`Command: `, commandType)
  //console.log(`Parameters: `, params)

  const changeCommandType = (e: any) => {
    setCommandType(mainCommands.find(cmd => cmd.id == +e.target.value) || null)
    const parameters = commandType?.params?.split(",") || []
    let paramsObject : { [key: string]: string } = {}
    for(const param of parameters) {
      paramsObject[param] = ""
    }
    setParams(paramsObject);
  }

  const changeParam = (e: any) => {
    const param = e.target.id
    const value = e.target.value

    setParams(prevParams => ({
      ...prevParams,
      [param]: value,
    }));
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            {/* TODO: (Member) Display the list of commands based on the get commands request*/}
            <select 
              value={commandType ? commandType.id : ""} 
              onChange={changeCommandType}>
              {mainCommands.map(cmd => (<option value={cmd.id}>{cmd.name}</option>))}
            </select>
          </div>
        
           {/* TODO: (Member) Add input handling here if the selected command has a param input*/}
          {commandType && 
            commandType.params?.split(",").map((param) => (<input id={param} placeholder={`Enter ${param}`} onChange={changeParam}/>))}
          <button type="submit">Submit</button>
        </div>
      </form>
    </> 
  )
}

export default CommandInput;
