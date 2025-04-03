import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import AppLayout from '../components/AppLayout';

// Mock the child components
vi.mock('../components/Sidebar', () => ({
  default: () => <div data-testid="sidebar">Sidebar Mock</div>,
}));

vi.mock('react-router', () => ({
  Outlet: () => <div data-testid="outlet">Outlet Mock</div>,
}));

describe('AppLayout Component', () => {
  it('renders the basic layout structure', () => {
    render(<AppLayout />);

    // Get the outermost container by finding the header's parent
    const container = screen.getByRole('banner').parentElement;
    expect(container).toHaveClass(
      'flex', 'flex-col', 'min-h-screen', 'h-screen',
      'bg-gray-800', 'text-white', 'items-center', 'justify-center'
    );

    // Check header
    const header = screen.getByRole('banner');
    expect(header).toHaveClass('text-center', 'border-b', 'border-gray-600', 'p-4', 'w-full');
    expect(screen.getByRole('heading', { name: /how can i help\?/i })).toBeInTheDocument();

    // Check content area (the flex container that holds Sidebar and main)
    const contentArea = screen.getByTestId('sidebar').parentElement;
    expect(contentArea).toHaveClass('flex', 'h-full', 'w-full');

    // Check main content area
    const main = screen.getByRole('main');
    expect(main).toHaveClass('w-full');

    // Verify mocked components are rendered
    expect(screen.getByTestId('sidebar')).toBeInTheDocument();
    expect(screen.getByTestId('outlet')).toBeInTheDocument();
  });

  it('has correct header text and styling', () => {
    render(<AppLayout />);
    
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('How can I help?');
    expect(heading).toHaveClass('text-2xl', 'font-bold');
  });
});