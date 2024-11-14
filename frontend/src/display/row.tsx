import { CommandStatusMapping } from "../data/other";
import { CommandResponse } from "../data/response";

interface CommandRowProp extends CommandResponse {
  handleDelete: () => void;
}

const CommandRow = ({ id, command_type, params, status, created_on, updated_on, handleDelete }: CommandRowProp) => {
  return (
    <tr>
      <th>{id}</th>
      <th>{command_type}</th>
      <th>{params}</th>
      <th>{CommandStatusMapping[status]}</th>
      <th>{created_on}</th>
      <th>{updated_on}</th>
      <th><button onClick={handleDelete}>Delete {id}</button></th>
    </tr>
  )
}

export default CommandRow;
