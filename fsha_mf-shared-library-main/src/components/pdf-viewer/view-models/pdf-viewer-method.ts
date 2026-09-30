/* eslint-disable @typescript-eslint/no-explicit-any */
/**
 * Methods interface for programmatically controlling the PDF Viewer component.
 *
 * This interface defines all available methods that can be called on the PDF viewer
 * component instance to control its behavior, navigate through documents, and interact
 * with the viewer programmatically. Most methods return Promises for asynchronous operations.
 *
 * ## Available Methods
 *
 * ### Navigation & Page Control
 * - `refresh()` - Refresh/reload the viewer (synchronous)
 * - `goToPage(page)` - Navigate to a specific page number
 * - `setPage(page)` - Set the current page (alternative to goToPage)
 * - `goToLastPage()` - Navigate to the last page
 * - `reloadViewer()` - Reload the viewer (alias of refresh)
 *
 * ### Display & View Control
 * - `setZoom(zoom)` - Set zoom level programmatically
 * - `setCursor(cursor)` - Change cursor type
 * - `setScroll(scroll)` - Change scroll mode
 * - `setSpread(spread)` - Change spread mode
 * - `setPageMode(mode)` - Set sidebar/page mode
 *
 * ### Actions & Operations
 * - `triggerDownload()` - Programmatically trigger PDF download
 * - `triggerPrint()` - Programmatically trigger print dialog
 * - `triggerRotation(direction)` - Rotate document programmatically
 *
 * ### Action Queue Management
 * - `sendViewerControlMessage(action, payload)` - Send custom control message
 * - `getActionStatus(actionId)` - Get status of a queued action
 * - `getQueueStatus()` - Get overall queue status
 * - `clearActionQueue()` - Clear all queued actions
 *
 * ### Window & Navigation
 * - `goBack()` - Navigate back in browser history
 * - `closeViewer()` - Close the viewer window
 *
 * ### Error & Validation
 * - `getErrorTemplateData()` - Get error template data
 * - `setUrlValidation(enabled)` - Enable/disable URL validation
 * - `dismissSecurityWarning()` - Dismiss security warning
 *
 * @example
 * ```typescript
 * // Access viewer methods via ViewChild
 * @ViewChild('pdfViewer') pdfViewer!: PdfJsViewerComponent;
 *
 * // Navigate to page 5
 * await this.pdfViewer.goToPage(5);
 *
 * // Set zoom level
 * await this.pdfViewer.setZoom('150%');
 *
 * // Trigger download
 * await this.pdfViewer.triggerDownload();
 * ```
 *
 * @example
 * ```typescript
 * // Rotate document
 * await this.pdfViewer.triggerRotation('cw'); // Clockwise
 * await this.pdfViewer.triggerRotation('ccw'); // Counter-clockwise
 *
 * // Change scroll mode
 * await this.pdfViewer.setScroll('horizontal');
 *
 * // Check action queue status
 * const status = this.pdfViewer.getQueueStatus();
 * console.log(`Queued: ${status.queuedActions}, Executed: ${status.executedActions}`);
 * ```
 *
 * @since 1.0.0
 */
export interface PdfViewerMethods {
  /**
   * Refresh or reload the PDF viewer.
   *
   * Reloads the current PDF document and resets the viewer state.
   * This is a synchronous operation (does not return a Promise).
   *
   * @example
   * ```typescript
   * pdfViewer.refresh();
   * ```
   */
  refresh(): void;

  /**
   * Navigate to a specific page number in the PDF document.
   *
   * Page numbers are 1-indexed (first page is 1, not 0).
   * Returns a Promise that resolves when navigation is complete.
   *
   * @param page - The page number to navigate to (1-indexed)
   * @returns Promise that resolves when page navigation is complete
   * @example
   * ```typescript
   * await pdfViewer.goToPage(10); // Go to page 10
   * ```
   */
  goToPage?: (page: number) => Promise<any>;

  /**
   * Set the current page (alternative to `goToPage`).
   *
   * Functionally equivalent to `goToPage`, but uses different naming convention.
   * Page numbers are 1-indexed.
   *
   * @param page - The page number to set (1-indexed)
   * @returns Promise that resolves when page is set
   * @example
   * ```typescript
   * await pdfViewer.setPage(5);
   * ```
   */
  setPage?: (page: number) => Promise<any>;

  /**
   * Set the zoom level programmatically.
   *
   * Accepts the same zoom values as the `zoom` input property:
   * - Predefined: 'auto', 'page-width', 'page-height', 'page-fit'
   * - Percentage: '50%', '125%', '200%', etc.
   * - Number as string: '1.5' (150%), '2' (200%), etc.
   *
   * @param zoom - Zoom level as string
   * @returns Promise that resolves when zoom is applied
   * @example
   * ```typescript
   * await pdfViewer.setZoom('150%');
   * await pdfViewer.setZoom('page-width');
   * await pdfViewer.setZoom('2'); // 200%
   * ```
   */
  setZoom?: (zoom: string) => Promise<any>;

  /**
   * Set the cursor type displayed when hovering over the PDF.
   *
   * @param cursor - Cursor type: 'select', 'hand', or 'zoom'
   * @returns Promise that resolves when cursor is changed
   * @example
   * ```typescript
   * await pdfViewer.setCursor('hand'); // Hand cursor for clickable elements
   * await pdfViewer.setCursor('zoom'); // Zoom cursor
   * await pdfViewer.setCursor('select'); // Text selection cursor
   * ```
   */
  setCursor?: (cursor: 'select' | 'hand' | 'zoom') => Promise<any>;

  /**
   * Set the scroll mode for navigating through PDF pages.
   *
   * @param scroll - Scroll mode: 'vertical', 'horizontal', 'wrapped', or 'page'
   * @returns Promise that resolves when scroll mode is changed
   * @example
   * ```typescript
   * await pdfViewer.setScroll('horizontal'); // Horizontal scrolling
   * await pdfViewer.setScroll('wrapped'); // Continuous flow
   * await pdfViewer.setScroll('vertical'); // Default vertical scrolling
   * ```
   */
  setScroll?: (scroll: 'vertical' | 'horizontal' | 'wrapped' | 'page') => Promise<any>;

  /**
   * Set the spread mode for displaying pages side-by-side.
   *
   * @param spread - Spread mode: 'none', 'odd', or 'even'
   * @returns Promise that resolves when spread mode is changed
   * @example
   * ```typescript
   * await pdfViewer.setSpread('odd'); // Odd pages on left
   * await pdfViewer.setSpread('even'); // Even pages on left
   * await pdfViewer.setSpread('none'); // Single page view
   * ```
   */
  setSpread?: (spread: 'none' | 'odd' | 'even') => Promise<any>;

  /**
   * Set the sidebar/page mode (what is displayed in the sidebar).
   *
   * @param mode - Page mode: 'none', 'thumbs', 'bookmarks', or 'attachments'
   * @returns Promise that resolves when page mode is changed
   * @example
   * ```typescript
   * await pdfViewer.setPageMode('thumbs'); // Show thumbnails
   * await pdfViewer.setPageMode('bookmarks'); // Show bookmarks/outline
   * await pdfViewer.setPageMode('attachments'); // Show attachments
   * ```
   */
  setPageMode?: (mode: 'none' | 'thumbs' | 'bookmarks' | 'attachments') => Promise<any>;

  /**
   * Programmatically trigger the PDF download.
   *
   * Initiates the download of the current PDF document.
   * The download will use the filename specified in `downloadFileName` input property.
   *
   * @returns Promise that resolves when download is triggered
   * @example
   * ```typescript
   * await pdfViewer.triggerDownload();
   * ```
   */
  triggerDownload?: () => Promise<any>;

  /**
   * Programmatically trigger the print dialog.
   *
   * Opens the browser's print dialog for the PDF document.
   *
   * @returns Promise that resolves when print dialog is opened
   * @example
   * ```typescript
   * await pdfViewer.triggerPrint();
   * ```
   */
  triggerPrint?: () => Promise<any>;

  /**
   * Rotate the PDF document programmatically.
   *
   * @param direction - Rotation direction: 'cw' (clockwise) or 'ccw' (counter-clockwise)
   * @returns Promise that resolves when rotation is applied
   * @example
   * ```typescript
   * await pdfViewer.triggerRotation('cw'); // Rotate 90° clockwise
   * await pdfViewer.triggerRotation('ccw'); // Rotate 90° counter-clockwise
   * ```
   */
  triggerRotation?: (direction: 'cw' | 'ccw') => Promise<any>;

  /**
   * Navigate to the last page of the PDF document.
   *
   * @returns Promise that resolves when navigation to last page is complete
   * @example
   * ```typescript
   * await pdfViewer.goToLastPage();
   * ```
   */
  goToLastPage?: () => Promise<any>;

  /**
   * Send a custom control message to the viewer.
   *
   * Allows sending custom commands or messages to the underlying PDF.js viewer
   * for advanced control scenarios.
   *
   * @param action - The action/command name to send
   * @param payload - Optional payload data for the action
   * @returns Promise that resolves with the action result
   * @example
   * ```typescript
   * await pdfViewer.sendViewerControlMessage('customAction', { data: 'value' });
   * ```
   */
  sendViewerControlMessage?: (action: string, payload: any) => Promise<any>;

  /**
   * Get the status of a specific queued action.
   *
   * Useful for tracking the progress of asynchronous operations.
   *
   * @param actionId - The unique identifier of the action
   * @returns Promise that resolves with the action status, or null if not found
   * @example
   * ```typescript
   * const status = await pdfViewer.getActionStatus('action-123');
   * if (status) {
   *   console.log('Action status:', status);
   * }
   * ```
   */
  getActionStatus?: (actionId: string) => Promise<any | null>;

  /**
   * Get the overall status of the action queue.
   *
   * Returns information about queued and executed actions.
   * This is a synchronous method (does not return a Promise).
   *
   * @returns Object containing queue statistics:
   * - `queuedActions`: Number of actions waiting in queue
   * - `executedActions`: Number of actions that have been executed
   * @example
   * ```typescript
   * const status = pdfViewer.getQueueStatus();
   * console.log(`Queued: ${status.queuedActions}, Executed: ${status.executedActions}`);
   * ```
   */
  getQueueStatus?: () => {
    queuedActions: number;
    executedActions: number;
  };

  /**
   * Clear all actions from the action queue.
   *
   * Cancels any pending actions that haven't been executed yet.
   * This is a synchronous operation.
   *
   * @example
   * ```typescript
   * pdfViewer.clearActionQueue();
   * ```
   */
  clearActionQueue?: () => void;

  /**
   * Reload the viewer (alias of `refresh`).
   *
   * Functionally equivalent to calling `refresh()`.
   * This is a synchronous operation.
   *
   * @example
   * ```typescript
   * pdfViewer.reloadViewer();
   * ```
   */
  reloadViewer?: () => void;

  /**
   * Navigate back in browser history.
   *
   * Only applicable when the viewer is in an external window.
   * This is a synchronous operation.
   *
   * @example
   * ```typescript
   * pdfViewer.goBack();
   * ```
   */
  goBack?: () => void;

  /**
   * Close the viewer window.
   *
   * Only applicable when the viewer is in an external window.
   * This is a synchronous operation.
   *
   * @example
   * ```typescript
   * pdfViewer.closeViewer();
   * ```
   */
  closeViewer?: () => void;

  /**
   * Get error template data.
   *
   * Retrieves data related to the current error state, useful for
   * custom error handling or logging.
   *
   * @returns Error template data object
   * @example
   * ```typescript
   * const errorData = pdfViewer.getErrorTemplateData();
   * if (errorData) {
   *   console.error('Error details:', errorData);
   * }
   * ```
   */
  getErrorTemplateData?: () => any;

  /**
   * Enable or disable URL validation for PDF sources.
   *
   * When enabled, validates PDF source URLs before attempting to load them.
   *
   * @param enabled - Whether to enable URL validation
   * @returns Promise that resolves when validation setting is updated
   * @example
   * ```typescript
   * await pdfViewer.setUrlValidation(true); // Enable validation
   * await pdfViewer.setUrlValidation(false); // Disable validation
   * ```
   */
  setUrlValidation?: (enabled: boolean) => Promise<any>;

  /**
   * Dismiss any active security warnings.
   *
   * Hides security-related warning messages displayed to users.
   * This is a synchronous operation.
   *
   * @example
   * ```typescript
   * pdfViewer.dismissSecurityWarning();
   * ```
   */
  dismissSecurityWarning?: () => void;
}
