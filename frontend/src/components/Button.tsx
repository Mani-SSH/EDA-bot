import React from "react";

interface ButtonProps {
  label: string; // The text displayed on the button
  onClick: () => void; // Function to call on button click
}

const Button: React.FC<ButtonProps> = ({ label, onClick }) => {
  return <button onClick={onClick}>{label}</button>;
};

export default Button;
