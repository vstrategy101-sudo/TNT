/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import * as React from "react";

interface LogoProps {
  className?: string;
  dotColor?: string;
}

export default function Logo({ className = "h-8", dotColor = "#0052FF" }: LogoProps) {
  return (
    <svg
      viewBox="0 0 88 44"
      className={`${className} select-none`}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="tnt."
    >
      {/* First "t" letter */}
      <path
        d="M0,13.5 h5.5 v-6 h8 v6 h6.5 v8.5 h-6.5 v9 c0,2.2 1,3 3,3 h3 v7.5 c-4.2,0 -8.5,-0.3 -11.2,-3.5 C7,35 6.5,32 6.5,29 v-7 h-5.5 v-8.5 z"
        fill="currentColor"
      />
      {/* "n" letter */}
      <path
        d="M22,13.5 h8 v2.2 c1.8,-1.8 4.5,-2.8 8,-2.8 c6.5,0 11,4.2 11,11.5 v14.5 h-8.5 v-12 c0,-3 -1.2,-4.5 -3.8,-4.5 c-2.5,0 -4.2,1.8 -5.2,4 v12.5 h-8.5 v-27.9 z"
        fill="currentColor"
      />
      {/* Second "t" letter */}
      <path
        d="M54,13.5 h5.5 v-6 h8 v6 h6.5 v8.5 h-6.5 v9 c0,2.2 1,3 3,3 h3 v7.5 c-4.2,0 -8.5,-0.3 -11.2,-3.5 C61,35 60.5,32 60.5,29 v-7 h-5.5 v-8.5 z"
        fill="currentColor"
      />
      {/* Solid Accent Dot */}
      <circle cx="80.5" cy="33.5" r="4.5" fill={dotColor} />
    </svg>
  );
}
