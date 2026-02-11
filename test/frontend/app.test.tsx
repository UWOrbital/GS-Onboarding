import { describe, it, expect, vi, beforeEach, type Mock } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import axios from 'axios'
import App from '../../frontend/src/app'
import type { MainCommandResponse, CommandResponse } from '../../frontend/src/data/response'

vi.mock('axios')

const mockMainCommands: MainCommandResponse[] = [
  { id: 1, name: "Main Command 1", params: "time", format: "int 7 bytes", data_size: 7, total_size: 7 },
  { id: 2, name: "Main Command 2", params: "mode_state_number,time", format: "int 1 byte, int 7 bytes", data_size: 8, total_size: 8 },
]

const makeCommand = (overrides: Partial<CommandResponse> & { id: number; command_type: number }): CommandResponse => ({
  status: 1,
  params: null,
  created_on: "2025-01-01T00:00:00Z",
  updated_on: "2025-01-01T00:00:00Z",
  ...overrides,
})

const command1: CommandResponse = makeCommand({ id: 1, command_type: 1, params: "time: 10" })
const command2: CommandResponse = makeCommand({ id: 2, command_type: 2, params: "mode_state_number: 5, time: 20" })

/**
 * Sets up axios.get mock to handle initial page load API calls.
 * @param commands - Commands to return from GET /commands/
 */
function setupGetMocks(commands: CommandResponse[] = []) {
  ;(axios.get as Mock).mockImplementation((url: string) => {
    if (url.includes('/main-commands/')) {
      return Promise.resolve({ data: { data: mockMainCommands } })
    }
    if (url.includes('/commands/')) {
      return Promise.resolve({ data: { data: commands } })
    }
    return Promise.reject(new Error(`Unexpected GET: ${url}`))
  })
}

describe('App Integration Tests', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  // Scenario 1
  it('should load the page with dropdown options, default selection, empty table, and parameter inputs', async () => {
    setupGetMocks([])

    render(<App />)

    // Wait for main commands to load in the dropdown
    await waitFor(() => {
      expect(screen.getByText('Main Command 1')).toBeInTheDocument()
    })

    // Dropdown contains both main commands
    expect(screen.getByText('Main Command 2')).toBeInTheDocument()

    // Main Command 1 is selected by default
    const dropdown = screen.getByRole('combobox')
    expect(dropdown).toHaveValue('1')

    // Table is empty (no delete buttons means no command rows)
    expect(screen.queryByRole('button', { name: /Delete/i })).not.toBeInTheDocument()

    // The "time" input field is displayed for Main Command 1
    expect(screen.getByLabelText('time:')).toBeInTheDocument()
  })

  // Scenario 2
  it('should create a command with Main Command 1 and display it in the table', async () => {
    const user = userEvent.setup()
    setupGetMocks([])

    ;(axios.post as Mock).mockResolvedValueOnce({
      data: { data: command1 },
    })

    render(<App />)

    // Wait for page load
    await waitFor(() => {
      expect(screen.getByText('Main Command 1')).toBeInTheDocument()
    })

    // Main Command 1 should be selected by default
    const dropdown = screen.getByRole('combobox')
    expect(dropdown).toHaveValue('1')

    // Enter "10" in the time input
    const timeInput = screen.getByLabelText('time:')
    await user.type(timeInput, '10')

    // Click Submit
    const submitButton = screen.getByRole('button', { name: /Submit/i })
    await user.click(submitButton)

    // Verify the command appears in the table
    await waitFor(() => {
      expect(screen.getByText('time: 10')).toBeInTheDocument()
    })

    // Check row data
    expect(screen.getByText('1')).toBeInTheDocument() // ID
    expect(screen.getByText('Scheduled')).toBeInTheDocument() // Status (index 1)

    // Check timestamps are present and match ISO format
    const isoRegex = /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/
    expect(screen.getByText(isoRegex)).toBeInTheDocument()

    // Delete button present
    expect(screen.getByRole('button', { name: 'Delete 1' })).toBeInTheDocument()
  })

  // Scenario 3
  it('should create a command with Main Command 2 showing two input fields', async () => {
    const user = userEvent.setup()
    setupGetMocks([command1])

    ;(axios.post as Mock).mockResolvedValueOnce({
      data: { data: command2 },
    })

    render(<App />)

    // Wait for page load
    await waitFor(() => {
      expect(screen.getByText('Main Command 1')).toBeInTheDocument()
    })

    // Select Main Command 2 from dropdown
    const dropdown = screen.getByRole('combobox')
    await user.selectOptions(dropdown, '2')

    // Verify two input fields appear
    await waitFor(() => {
      expect(screen.getByLabelText('mode_state_number:')).toBeInTheDocument()
      expect(screen.getByLabelText('time:')).toBeInTheDocument()
    })

    // Enter values
    await user.type(screen.getByLabelText('mode_state_number:'), '5')
    await user.type(screen.getByLabelText('time:'), '20')

    // Click Submit
    await user.click(screen.getByRole('button', { name: /Submit/i }))

    // Verify new command appears in the table
    await waitFor(() => {
      expect(screen.getByText('mode_state_number: 5, time: 20')).toBeInTheDocument()
    })

    // Check row data for command 2
    expect(screen.getByRole('button', { name: 'Delete 2' })).toBeInTheDocument()
  })

  // Scenario 4
  it('should delete a command and keep remaining commands in the table', async () => {
    const user = userEvent.setup()
    setupGetMocks([command1, command2])

    ;(axios.delete as Mock).mockResolvedValueOnce({
      data: { data: [command2] },
    })

    render(<App />)

    // Wait for both commands to load
    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Delete 1' })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'Delete 2' })).toBeInTheDocument()
    })

    // Click Delete on command 1
    await user.click(screen.getByRole('button', { name: 'Delete 1' }))

    // Command 1 should be removed
    await waitFor(() => {
      expect(screen.queryByRole('button', { name: 'Delete 1' })).not.toBeInTheDocument()
    })

    // Command 2 should still be displayed
    expect(screen.getByRole('button', { name: 'Delete 2' })).toBeInTheDocument()
  })

  // Scenario 5
  it('should delete all commands leaving an empty table, and app still functions', async () => {
    const user = userEvent.setup()
    setupGetMocks([command2])

    ;(axios.delete as Mock).mockResolvedValueOnce({
      data: { data: [] },
    })

    render(<App />)

    // Wait for command to load
    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Delete 2' })).toBeInTheDocument()
    })

    // Click Delete on command 2
    await user.click(screen.getByRole('button', { name: 'Delete 2' }))

    // Table should be empty
    await waitFor(() => {
      expect(screen.queryByRole('button', { name: /Delete/i })).not.toBeInTheDocument()
    })

    // App still functions - dropdown and submit button are still present
    expect(screen.getByRole('combobox')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Submit/i })).toBeInTheDocument()
  })
})
