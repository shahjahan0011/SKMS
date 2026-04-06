import { render, screen } from '@testing-library/react';
import App from './App';

test('renders frontend title', () => {
  render(<App />);
  expect(screen.getByText(/SKMS Food Delivery Frontend/i)).toBeInTheDocument();
});
