import React, { ReactElement, useEffect, useState } from "react"
import "./command_input.css"
import { MainCommandListResponse, MainCommandResponse } from "../data/response"
import { createCommand, getMainCommands } from "./input_api"
import { CommandRequest } from "../data/request"


const CommandInput = () => {
  // TODO: (Member) Setup state and useEffect calls here
  
  
  const handleSubmit = async (e:React.FormEvent) => {
    // TODO:(Member) Submit to your post endpoint
     
  }

  return (
    <>
      <form>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select>
              <option value={"1"}>Command 1</option>
              <option value={"2"}>Command 2</option>
              <option value={"3"}>Command3</option>
            </select>
          </div>
          <input/> {/* TODO: (Member) Add input handling here if the selected command has a param input*/}
          <button onClick={handleSubmit}>Submit</button>
        </div>
      </form>
    </>
  )
}

export default CommandInput;
