import React from "react";

interface Props {
  color?: string;
  size?: number;
}

const RotateIcon = ({ color = "#003e5b", size = 15 }: Props) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlnsXlink="http://www.w3.org/1999/xlink"
      fill="#000000"
      version="1.1"
      id="Capa_1"
      viewBox="0 0 214.367 214.367"
      xmlSpace="preserve"
      width={size}
      height={size}
      transform="rotate(270)"
    >
      <path
        fill={color}
        d="M202.403,95.22c0,46.312-33.237,85.002-77.109,93.484v25.663l-69.76-40l69.76-40v23.494  c27.176-7.87,47.109-32.964,47.109-62.642c0-35.962-29.258-65.22-65.22-65.22s-65.22,29.258-65.22,65.22  c0,9.686,2.068,19.001,6.148,27.688l-27.154,12.754c-5.968-12.707-8.994-26.313-8.994-40.441C11.964,42.716,54.68,0,107.184,0  S202.403,42.716,202.403,95.22z"
      />
    </svg>
  );
};

export default RotateIcon;
