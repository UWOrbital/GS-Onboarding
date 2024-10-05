const CommandInput = () => {
  return (
    <>
      <form>
        <label>Command Type: </label>
        <select>
          <option value="1">Command 1</option>
          <option value="2">Command 2</option>
          <option value="3">Command 3</option>
        </select>
        <button type="submit">Submit</button>
      </form>
    </>
  )
}

export default CommandInput;
