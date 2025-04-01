import { render, screen} from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import PromptForm from '../components/PromptForm'
import { describe, it, expect, vi } from 'vitest'

// Mock the Loader2 icon
vi.mock('lucide-react', () => ({
  Loader2: () => <div data-testid="loader-icon" />,
}))

describe('PromptForm Component', () => {
  const mockProps = {
    systemText: 'You are a helpful assistant',
    userMessage: 'How are you?',
    isLoading: false,
    handleSystemTextChange: vi.fn(),
    handleUserMessageChange: vi.fn(),
    handleSubmit: vi.fn(),
  }

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders correctly with provided props', () => {
    render(<PromptForm {...mockProps} />)
    
    // Check labels
    expect(screen.getByText('System Text:')).toBeInTheDocument()
    expect(screen.getByText('User Message:')).toBeInTheDocument()
    
    // Check input values
    const systemInput = screen.getByDisplayValue(mockProps.systemText)
    const userInput = screen.getByDisplayValue(mockProps.userMessage)
    expect(systemInput).toBeInTheDocument()
    expect(userInput).toBeInTheDocument()
    
    // Check submit button
    expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument()
  })

  it('calls handleSystemTextChange when system text is changed', async () => {
    render(<PromptForm {...mockProps} />)
    
    const systemInput = screen.getByDisplayValue(mockProps.systemText)
    const newValue = 'You are a pirate'
    
    await userEvent.type(systemInput, newValue)
    
    expect(mockProps.handleSystemTextChange).toHaveBeenCalledTimes(newValue.length)
  })

  it('calls handleUserMessageChange when user message is changed', async () => {
    render(<PromptForm {...mockProps} />)
    
    const userInput = screen.getByDisplayValue(mockProps.userMessage)
    const newValue = ' Where is the treasure?'
    
    await userEvent.type(userInput, newValue)
    
    expect(mockProps.handleUserMessageChange).toHaveBeenCalledTimes(newValue.length)
  })

  it('calls handleSubmit when the button is clicked', async () => {
    render(<PromptForm {...mockProps} />)
    
    const submitButton = screen.getByRole('button', { name: 'Submit' })
    await userEvent.click(submitButton)
    
    expect(mockProps.handleSubmit).toHaveBeenCalledTimes(1)
  })

  it('disables the button and shows loader when isLoading is true', () => {
    render(<PromptForm {...mockProps} isLoading={true} />)
    
    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
    expect(button).toHaveClass('disabled:cursor-not-allowed')
    expect(screen.getByTestId('loader-icon')).toBeInTheDocument()
  })

  it('applies correct styling to inputs', () => {
    render(<PromptForm {...mockProps} />)
    
    const systemInput = screen.getByDisplayValue(mockProps.systemText)
    const userInput = screen.getByDisplayValue(mockProps.userMessage)
    
    expect(systemInput).toHaveClass('bg-neutral-700')
    expect(systemInput).toHaveClass('w-full')
    expect(systemInput).toHaveClass('p-4')
    expect(systemInput).toHaveClass('text-white')
    
    expect(userInput).toHaveClass('text-lg') // Specific to user message
  })

  it('applies correct styling to submit button', () => {
    render(<PromptForm {...mockProps} />)
    
    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-blue-500')
    expect(button).toHaveClass('text-white')
    expect(button).toHaveClass('w-full')
  })

  it('does not call handleSubmit when button is disabled', async () => {
    render(<PromptForm {...mockProps} isLoading={true} />)
    
    const button = screen.getByRole('button')
    await userEvent.click(button)
    
    expect(mockProps.handleSubmit).not.toHaveBeenCalled()
  })

  it('shows "Submit" text when not loading', () => {
    render(<PromptForm {...mockProps} isLoading={false} />)
    
    expect(screen.getByText('Submit')).toBeInTheDocument()
    expect(screen.queryByTestId('loader-icon')).not.toBeInTheDocument()
  })
})