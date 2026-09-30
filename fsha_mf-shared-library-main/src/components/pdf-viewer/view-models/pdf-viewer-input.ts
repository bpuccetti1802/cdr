/* eslint-disable @typescript-eslint/no-explicit-any */
import { TemplateRef } from '@angular/core';
import {
  AutoActionConfig,
  ControlVisibilityConfig,
  ErrorConfig,
  GroupVisibilityConfig,
  LayoutConfig,
  ThemeConfig,
  ViewerConfig,
} from 'ng2-pdfjs-viewer';
import { CursorType } from '../constants/cursor-type';
import { ScrollType } from '../constants/scroll-type';
import { SpreadType } from '../constants/spread-type';
import { PageMode } from '../constants/page-mode';

/**
 * Configuration interface for the PDF Viewer component.
 *
 * This interface defines all available input properties that can be passed to the PDF viewer
 * component to customize its appearance, behavior, and functionality. All properties are optional,
 * allowing for flexible configuration with sensible defaults.
 *
 * ## Available Properties
 *
 * ### Document Source & Basic Configuration
 * - `pdfSrc` - PDF document source (URL, Blob, or Uint8Array)
 * - `viewerId` - Unique viewer identifier
 * - `viewerFolder` - Path to PDF.js assets folder
 * - `externalWindow` - Open in new window/tab
 * - `externalWindowOptions` - Window options string
 * - `target` - Target attribute for external window
 *
 * ### Theming & Styling
 * - `theme` - UI theme ('light' | 'dark' | 'auto')
 * - `primaryColor` - Primary color for UI elements
 * - `backgroundColor` - Background color for viewer
 * - `pageBorderColor` - Page border color
 * - `toolbarColor` - Toolbar background color
 * - `textColor` - Text color in UI
 * - `borderRadius` - CSS border radius
 * - `customCSS` - Custom CSS styles
 * - `themeConfig` - Theme configuration object
 *
 * ### Customization Templates
 * - `iframeTitle` - Accessible iframe title
 * - `customSpinnerTpl` - Custom spinner template
 * - `spinnerClass` - Spinner CSS class
 * - `customErrorTpl` - Custom error template
 * - `errorClass` - Error CSS class
 * - `customSecurityTpl` - Custom security warning template
 *
 * ### Navigation & Display
 * - `page` - Initial page number (1-indexed)
 * - `namedDest` - Named destination to navigate to
 * - `rotation` - Document rotation angle (degrees)
 * - `zoom` - Zoom level ('auto', 'page-width', percentage, etc.)
 * - `cursor` - Cursor type ('HAND' | 'SELECT' | 'ZOOM')
 * - `scroll` - Scroll mode ('VERTICAL' | 'HORIZONTAL' | 'WRAPPED')
 * - `spread` - Spread mode ('ODD' | 'EVEN' | 'NONE')
 * - `pageMode` - Sidebar page mode ('none' | 'thumbs' | 'bookmarks' | 'attachments')
 *
 * ### Layout Configuration
 * - `layoutConfig` - Layout configuration object
 * - `groupVisibility` - Group visibility configuration
 * - `iframeBorder` - Iframe border width
 *
 * ### Auto Actions
 * - `autoActions` - Auto actions configuration object
 *
 * ### Error Handling
 * - `errorHandling` - Error handling configuration
 *
 * @example
 * ```typescript
 * const viewerConfig: PdfViewerInput = {
 *   pdfSrc: 'https://example.com/document.pdf',
 *   zoom: 'page-width',
 *   showDownload: true,
 *   showPrint: true,
 *   theme: 'light',
 *   locale: 'en-US'
 * };
 * ```
 *
 * @example
 * ```typescript
 * // Using with Blob
 * const blob = new Blob([pdfData], { type: 'application/pdf' });
 * const viewerConfig: PdfViewerInput = {
 *   pdfSrc: blob,
 *   showSpinner: true
 * };
 * ```
 *
 * @since 1.0.0
 */
export interface PdfViewerInput {
  /**
   * The PDF document source to display.
   *
   * Can be a URL string, Blob object, or Uint8Array containing PDF data.
   * This is the primary required property for the viewer to function.
   *
   * @example
   * ```typescript
   * pdfSrc: 'https://example.com/document.pdf'
   * pdfSrc: '/assets/documents/sample.pdf'
   * ```
   */
  pdfSrc?: string;

  /**
   * The PDF document source to display.
   *
   * Can be a Uint8Array or Blob containing PDF data.
   * This is the primary required property for the viewer to function.
   *
   * @example
   * ```typescript
   * pdfBlobUint8Array: new Uint8Array([...])
   * pdfBlobUint8Array: new Blob([...], { type: 'application/pdf' })
   * ```
   */
  pdfBlobUint8Array?: Uint8Array | Blob;

  /**
   * Unique identifier for the PDF viewer instance.
   *
   * Useful when multiple viewers are present on the same page.
   * If not provided, defaults to 'pdf-viewer'.
   *
   * @default 'pdf-viewer'
   * @example
   * ```typescript
   * viewerId: 'my-custom-viewer-123'
   * ```
   */
  viewerId?: string;

  /**
   * Path to the PDF.js viewer folder containing web/build assets.
   *
   * This should point to the location where PDF.js viewer files are hosted.
   * Typically located in the assets folder of your Angular application.
   *
   * @default 'assets/pdfjs'
   * @example
   * ```typescript
   * viewerFolder: 'assets/pdfjs'
   * viewerFolder: '/libs/pdfjs/web'
   * ```
   */
  viewerFolder?: string;

  /**
   * Whether to open the PDF document in a new window or tab.
   *
   * When set to `true`, the PDF will open in a popup window instead of
   * being embedded in the current page.
   *
   * @default false
   */
  externalWindow?: boolean;

  /**
   * Window options string for the external window (when `externalWindow` is true).
   *
   * Specifies the size, position, and other window features.
   * Uses the standard window.open() options format.
   *
   * @example
   * ```typescript
   * externalWindowOptions: 'width=800,height=600,left=100,top=100'
   * ```
   */
  externalWindowOptions?: string;

  /**
   * Target attribute for the external window.
   *
   * Standard HTML target values like '_blank' or '_self'.
   *
   * @default '_blank'
   */
  target?: string;

  /**
   * UI theme for the PDF viewer interface.
   *
   * - `'light'`: Light theme with light background
   * - `'dark'`: Dark theme with dark background
   * - `'auto'`: Automatically matches system preference
   *
   * @default 'light'
   */
  theme?: 'light' | 'dark' | 'auto';

  /**
   * Primary color for UI elements (e.g., toolbar buttons, highlights).
   *
   * Accepts any valid CSS color value (hex, rgb, named colors, etc.).
   *
   * @example
   * ```typescript
   * primaryColor: '#3498db'
   * primaryColor: 'rgb(52, 152, 219)'
   * primaryColor: 'blue'
   * ```
   */
  primaryColor?: string;

  /**
   * Background color for the viewer UI container.
   *
   * Accepts any valid CSS color value.
   *
   * @example
   * ```typescript
   * backgroundColor: '#f5f5f5'
   * backgroundColor: 'white'
   * ```
   */
  backgroundColor?: string;

  /**
   * Color for the border around PDF pages.
   *
   * Accepts any valid CSS color value.
   *
   * @example
   * ```typescript
   * pageBorderColor: '#ddd'
   * ```
   */
  pageBorderColor?: string;

  /**
   * Background color for the toolbar.
   *
   * Accepts any valid CSS color value.
   */
  toolbarColor?: string;

  /**
   * Text color used throughout the UI.
   *
   * Accepts any valid CSS color value.
   */
  textColor?: string;

  /**
   * CSS border radius for UI elements.
   *
   * Accepts any valid CSS border-radius value.
   *
   * @example
   * ```typescript
   * borderRadius: '8px'
   * borderRadius: '4px 8px'
   * borderRadius: '50%'
   * ```
   */
  borderRadius?: string;

  /**
   * Custom CSS styles to apply to the viewer wrapper.
   *
   * Can be used to override default styles or add custom styling.
   * Accepts a string of CSS rules.
   *
   * @example
   * ```typescript
   * customCSS: '.pdf-viewer { box-shadow: 0 2px 4px rgba(0,0,0,0.1); }'
   * ```
   */
  customCSS?: string;

  /**
   * Accessible title for the iframe element.
   *
   * Important for screen readers and accessibility compliance.
   *
   * @default 'PDF Viewer'
   */
  iframeTitle?: string;

  /**
   * Custom Angular template for the loading spinner/progress indicator.
   *
   * Allows complete customization of the loading state UI.
   * Use Angular's TemplateRef to pass a custom template.
   */
  customSpinnerTpl?: TemplateRef<any>;

  /**
   * Custom CSS class name for the spinner/progress indicator.
   *
   * Allows styling the default spinner without creating a custom template.
   *
   * @example
   * ```typescript
   * spinnerClass: 'my-custom-spinner'
   * ```
   */
  spinnerClass?: string;

  /**
   * Custom Angular template for error messages.
   *
   * Allows complete customization of error state UI.
   * Use Angular's TemplateRef to pass a custom template.
   */
  customErrorTpl?: TemplateRef<any>;

  /**
   * Custom CSS class name for error messages.
   *
   * Allows styling error messages without creating a custom template.
   */
  errorClass?: string;

  /**
   * Page number to display when the PDF loads.
   *
   * Page numbers are 1-indexed (first page is 1, not 0).
   * Can also be set programmatically after the viewer is initialized.
   *
   * @default 1
   * @example
   * ```typescript
   * page: 5  // Opens to page 5
   * ```
   */
  page?: number;

  /**
   * Named destination within the PDF to navigate to.
   *
   * Allows jumping to a specific section or bookmark defined in the PDF.
   * This is a PDF feature that uses internal PDF destinations.
   *
   * @example
   * ```typescript
   * namedDest: 'chapter-3'
   * ```
   */
  namedDest?: string;

  /**
   * Document rotation angle in degrees.
   *
   * Rotates the entire PDF document. Common values: 0, 90, 180, 270.
   * Supports two-way binding for programmatic rotation control.
   *
   * @default 0
   * @example
   * ```typescript
   * rotation: 90  // Rotate 90 degrees clockwise
   * ```
   */
  rotation?: number;

  /**
   * File name to use when downloading the PDF.
   *
   * Only used when the download functionality is triggered.
   *
   * @default 'documento.pdf'
   * @example
   * ```typescript
   * downloadFileName: 'invoice-2024.pdf'
   * ```
   */
  downloadFileName?: string;

  /**
   * Fine-grained control over individual control visibility.
   *
   * Provides more granular control than the boolean show/hide properties.
   * Allows showing/hiding specific controls within toolbar groups.
   *
   * @see ControlVisibilityConfig
   */
  controlVisibility?: ControlVisibilityConfig;

  /**
   * Configuration for automatic actions on PDF load.
   *
   * Groups all auto-action settings into a single configuration object.
   * Alternative to individual boolean properties like `downloadOnLoad`, `printOnLoad`, etc.
   *
   * @see AutoActionConfig
   */
  autoActions?: AutoActionConfig;

  /**
   * Configuration for error handling and error message display.
   *
   * Allows customization of error messages, error display behavior,
   * and error handling strategies.
   *
   * @see ErrorConfig
   */
  errorHandling?: ErrorConfig;

  /**
   * Advanced viewer configuration options.
   *
   * Provides low-level configuration for the underlying PDF.js viewer.
   * Use with caution as it may affect core functionality.
   *
   * @see ViewerConfig
   */
  viewerConfig?: ViewerConfig;

  /**
   * Theme configuration object.
   *
   * Alternative to individual theme properties. Allows more comprehensive
   * theme customization.
   *
   * @see ThemeConfig
   */
  themeConfig?: ThemeConfig;

  /**
   * Configuration for toolbar and sidebar group visibility.
   *
   * Provides control over entire groups of UI elements rather than
   * individual controls.
   *
   * @see GroupVisibilityConfig
   */
  groupVisibility?: GroupVisibilityConfig;

  /**
   * Layout configuration for the viewer.
   *
   * Groups layout-related settings like toolbar position, sidebar width,
   * and responsive breakpoints.
   *
   * @see LayoutConfig
   */
  layoutConfig?: LayoutConfig;

  /**
   * Whether to enable URL validation for PDF sources.
   *
   * When enabled, validates that the PDF source URL is valid before
   * attempting to load it. Can help prevent errors from invalid URLs.
   *
   * @default false
   */
  urlValidation?: boolean;

  /**
   * Custom Angular template for security warnings.
   *
   * Allows customization of security-related warning messages
   * displayed to users.
   */
  customSecurityTpl?: TemplateRef<any>;

  /**
   * Border width for the iframe element.
   *
   * Accepts CSS border-width values (px, em, etc.) or a number (pixels).
   *
   * @default '0'
   * @example
   * ```typescript
   * iframeBorder: '1px'
   * iframeBorder: 2
   * ```
   */
  iframeBorder?: string | number;

  /**
   * Initial zoom level for the PDF document.
   *
   * Accepts predefined values or percentage strings:
   * - `'auto'`: Automatic zoom based on container size
   * - `'page-width'`: Fit page width to container
   * - `'page-height'`: Fit page height to container
   * - `'page-fit'`: Fit entire page to container
   * - Percentage: `'50%'`, `'150%'`, etc.
   * - Number as string: `'1.5'` (150%)
   *
   * @default 'page-width'
   * @example
   * ```typescript
   * zoom: 'auto'
   * zoom: 'page-width'
   * zoom: '125%'
   * zoom: '2'  // 200%
   * ```
   */
  zoom?: string;

  /**
   * Cursor type to display when hovering over the PDF.
   *
   * - `'HAND'Hand cursor (for clickable elements)
   * - `'SELECT': Text selection cursor
   * - `'ZOOM': Zoom cursor (magnifying glass)
   *
   * @default 'SELECT'
   */
  cursor?: CursorType;

  /**
   * Scroll mode for navigating through PDF pages.
   *
   * - `'vertical'`: Vertical scrolling (default)
   * - `'horizontal'`: Horizontal scrolling
   * - `'wrapped'`: Wrapped scrolling (continuous flow)
   * - `'page'`: Page scrolling
   *
   * @default 'vertical'
   */
  scroll?: ScrollType;

  /**
   * Spread mode for displaying pages side-by-side.
   *
   * - `'odd'`: Show odd pages on left, even on right
   * - `'even'`: Show even pages on left, odd on right
   * - `'none'`: Single page view (no spread)
   *
   * @default 'none'
   */
  spread?: SpreadType;

  /**
   * Initial page mode for the sidebar.
   *
   * Controls what is displayed in the sidebar when it's open:
   * - `'none'`: No sidebar content
   * - `'thumbs'`: Page thumbnails
   * - `'bookmarks'`: Document outline/bookmarks
   * - `'attachments'`: Document attachments
   *
   * @default 'none'
   */
  pageMode?: PageMode;

  /**
   * Whether to show a spinner/progress indicator while the PDF is loading.
   *
   * Provides visual feedback during document loading. Can be customized
   * with `customSpinnerTpl` or `spinnerClass`.
   *
   * @default true
   */
  showSpinner?: boolean;

  /**
   * Locale for the viewer UI (toolbar buttons, messages, etc.).
   *
   * Uses BCP 47 language tags (e.g., 'en-US', 'de-AT', 'fr-FR', 'it-IT').
   * Affects button labels, tooltips, and other UI text.
   *
   * @default 'en-US'
   * @example
   * ```typescript
   * locale: 'en-US'  // English (United States)
   * locale: 'de-AT'  // German (Austria)
   * locale: 'it-IT'  // Italian (Italy)
   * ```
   */
  locale?: string;

  /**
   * Whether to use only CSS-based zoom instead of canvas scaling.
   *
   * CSS zoom is generally better for mobile devices and provides
   * smoother performance, but may have limitations with some PDF features.
   *
   * @default false
   * @recommended Set to `true` for mobile-optimized applications
   */
  useOnlyCssZoom?: boolean;

  /**
   * Whether to enable diagnostic logging to the console.
   *
   * Useful for debugging PDF loading issues and viewer behavior.
   * Should be disabled in production for performance and security.
   *
   * @default false
   * @warning Enabling this may expose sensitive information in console logs
   */
  diagnosticLogs?: boolean;
}
