import { useEffect, useState } from "react"
import { CommandResponse } from "../data/response"
import { getCommands, deleteCommand } from "./command_api"
import CommandRow from "./row"

const CommandTable = () => {
  const [commands, setCommands] = useState<CommandResponse[]>([])

  useEffect(() => {
    const getCommandsFn = async () => {
      const data = await getCommands();
      setCommands(data.data);
    }

    getCommandsFn();
  }, [])
  const handleDelete = (id: number) => {
    return async () => {
      // TODO: (Member) Handle delete logic here
      // You will need to create a function in `command_api.ts` before you can finish this part.
      try {
        const response  = await deleteCommand(id);
        setCommands(response.data);
      } catch (error) {
        alert("Error deleting item");
        console.error("Error deleting item: ", error)
      }
    }
  }

  return (
    <table>
      <thead>
        <tr>
          <th>ID: </th>
          <th>Main Command ID: </th>
          <th>Params: </th>
          <th>Status: </th>
          <th>Created On: </th>
          <th>Updated On: </th>
          <th>Delete</th>
        </tr>
      </thead>
      <thead>
        {commands.map(value => (<CommandRow {...value} handleDelete={handleDelete(value.id)} />))}
      </thead>
    </table>
  )
}

export default CommandTable;
