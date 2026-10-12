import React from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

export const Tex: React.FC<{
  tex: string;
  size?: number;
  color?: string;
  style?: React.CSSProperties;
}> = ({tex, size = 44, color = '#F4F7FB', style}) => {
  const html = katex.renderToString(tex, {displayMode: true, throwOnError: false, output: 'html'});
  return (
    <div
      style={{fontSize: size, color, lineHeight: 1.2, ...style}}
      dangerouslySetInnerHTML={{__html: html}}
    />
  );
};
