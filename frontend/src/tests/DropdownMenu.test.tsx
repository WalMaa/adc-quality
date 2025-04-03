import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Dropdown from '../components/DropdownMenu';
import { describe, it, expect, vi } from 'vitest'

interface DropdownOption {
    value: string;
    label: string;
  }

describe('Dropdown Component', () => {
  const mockOptions: DropdownOption[] = [
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3' },
  ]

  it('renders with default option', () => {
    render(
      <Dropdown
        options={mockOptions}
        defaultOption={mockOptions[0]}
      />
    )
    
    expect(screen.getByText('Option 1')).toBeInTheDocument()
  })

  it('renders with "Select an option" when no default provided', () => {
    render(<Dropdown options={mockOptions} />)
    
    expect(screen.getByText('Select an option')).toBeInTheDocument()
  })

  it('opens dropdown when clicked', async () => {
    render(<Dropdown options={mockOptions} />)
    
    const button = screen.getByRole('button')
    await userEvent.click(button)
    
    expect(screen.getByText('Option 1')).toBeVisible()
    expect(screen.getByText('Option 2')).toBeVisible()
    expect(screen.getByText('Option 3')).toBeVisible()
  })

  it('calls onSelect when an option is clicked', async () => {
    const mockOnSelect = vi.fn()
    render(
      <Dropdown
        options={mockOptions}
        onSelect={mockOnSelect}
      />
    )
    
    const button = screen.getByRole('button')
    await userEvent.click(button)
    
    const option2 = screen.getByText('Option 2')
    await userEvent.click(option2)
    
    expect(mockOnSelect).toHaveBeenCalledWith(mockOptions[1])
    expect(screen.getByText('Option 2')).toBeInTheDocument()
  })

  it('closes dropdown when clicking outside', async () => {
    render(
      <div>
        <Dropdown options={mockOptions} />
        <div data-testid="outside-element">Outside Element</div>
      </div>
    );
  
    const button = screen.getByRole('button');
    await userEvent.click(button);
    expect(screen.getByText('Option 1')).toBeVisible();
  
    const outsideElement = screen.getByTestId('outside-element');
    await userEvent.click(outsideElement);
    expect(screen.queryByText('Option 1')).toBeNull();
  });

  it('displays "No AI models found" when options are empty', () => {
    render(<Dropdown options={[]} />)
    
    const button = screen.getByRole('button')
    fireEvent.click(button)
    
    expect(screen.getByText('No AI models found')).toBeInTheDocument()
  })

  it('updates selected option when defaultOption prop changes', () => {
    const { rerender } = render(
      <Dropdown
        options={mockOptions}
        defaultOption={mockOptions[0]}
      />
    )
    
    expect(screen.getByText('Option 1')).toBeInTheDocument()
    
    rerender(
      <Dropdown
        options={mockOptions}
        defaultOption={mockOptions[1]}
      />
    )
    
    expect(screen.getByText('Option 2')).toBeInTheDocument()
  })
})