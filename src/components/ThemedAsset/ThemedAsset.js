// src/components/ThemedAsset.js
import React from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import clsx from 'clsx'; // Optional: for combining class names

/**
 * Renders a different asset (passed as a React component) based on the current theme.
 * Useful for theme-specific SVG components required from relative paths.
 *
 * @param {object} props
 * @param {React.ComponentType} props.lightSource - The React component for the light theme asset.
 * @param {React.ComponentType} props.darkSource - The React component for the dark theme asset.
 * @param {string} [props.className] - Optional CSS class(es) to apply to the rendered component.
 * @param {object} [props.style] - Optional inline styles.
 * @param {string} [props.ariaLabel] - Accessibility label.
 * // Add any other props you expect your SVG components might need (e.g., width, height - though style is often better)
 */
// export default function ThemedAsset({
//   lightSource: LightComponent, // Rename props internally for clarity
//   darkSource: DarkComponent,
//   className, // Destructure known props
//   ...restProps // Capture any other props (like style, aria-label, etc.)
// }) {
//   const { colorMode } = useColorMode();

//   // Determine which component to render
//   const ComponentToRender = colorMode === 'dark' ? DarkComponent : LightComponent;

//   // Handle cases where one of the sources might be missing
//   if (!ComponentToRender) {
//     console.warn(
//       'ThemedAsset: The required source component for the current theme (' +
//       colorMode +
//       ') is missing.'
//     );
//     // Optionally render a placeholder or null
//     // For example: return <div style={{ width: 24, height: 24, display: 'inline-block', border: '1px dashed red' }} title="Missing asset"></div>;
//     return null;
//   }

//   // Render the selected component, passing down the className and any other props
//   return <ComponentToRender className={clsx(className)}
  
//       {...restProps} 
//     />;
// }

export default function ThemedAsset(props) {
  const {
    lightSource, // Can be URL string or Component
    darkSource,  // Can be URL string or Component
    className,
    alt,        // Use alt for img tags
    ariaLabel,  // Use aria-label for SVG components
    ...restProps // Capture other props like style, etc.
  } = props;

  const { colorMode } = useColorMode();
  const isDarkTheme = colorMode === 'dark';

  const Source = isDarkTheme ? darkSource : lightSource;

  // Handle missing source gracefully
  if (!Source) {
    console.warn(
      `ThemedAsset: Source for theme "${colorMode}" is missing.`
    );
    return null; // Or return a placeholder
  }

  // Check the type of the source to decide how to render
  if (typeof Source === 'string') {
    // It's a URL string, render an <img> tag
    // Use 'alt' prop for accessibility
    return (
      <img
        src={Source}
        alt={alt || ariaLabel || ''} // Use alt, fallback to ariaLabel or empty
        className={clsx(className)}
        {...restProps} // Pass style, etc.
      />
    );
  } else if (typeof Source === 'function' || typeof Source === 'object') {
    // It's likely a React component (function or class, or object from require)
    // Use 'aria-label' prop for accessibility, add role="img"
    // Assign to a variable starting with uppercase for JSX rendering
    const ComponentToRender = Source;
    return (
      <ComponentToRender
        className={clsx(className)}
        aria-label={ariaLabel || alt || ''} // Use aria-label, fallback to alt or empty
        role="img" // Add role img for semantic meaning
        {...restProps} // Pass style, etc.
      />
    );
  } else {
    // Log an error if the source type is unexpected
    console.error('ThemedAsset: Received an unexpected source type:', Source);
    return null;
  }
}