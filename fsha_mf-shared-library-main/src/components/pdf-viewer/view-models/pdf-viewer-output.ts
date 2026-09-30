/* eslint-disable @typescript-eslint/no-explicit-any */
import { EventEmitter } from '@angular/core';
import {
  AnnotationLayerRenderEvent,
  BookmarkClick,
  ChangedRotation,
  ChangedScale,
  DocumentError,
  DocumentOutline,
  FindMatchesCount,
  PagesInfo,
  PresentationMode,
} from 'ng2-pdfjs-viewer';

/**
 * Output events interface for the PDF Viewer component.
 *
 * This interface defines all available output events (EventEmitters) that the PDF viewer
 * component can emit to notify parent components about various state changes, user interactions,
 * and document lifecycle events. All events are optional and can be subscribed to in the template
 * or programmatically.
 *
 * ## Available Events
 *
 * ### Document Lifecycle Events
 * - `onDocumentLoad` - Emitted when PDF document is successfully loaded
 * - `onDocumentInit` - Emitted when document is initialized
 * - `onDocumentError` - Emitted when document loading fails
 *
 * ### Navigation & Page Events
 * - `onPageChange` - Emitted when current page changes
 * - `onPagesInit` - Emitted when pages are initialized
 *
 * ### View & Display Events
 * - `onScaleChange` - Emitted when zoom/scale changes
 * - `onRotationChange` - Emitted when document rotation changes
 * - `onPresentationModeChanged` - Emitted when presentation mode changes
 * - `zoomChange` - Emitted when zoom level changes
 * - `cursorChange` - Emitted when cursor type changes
 * - `scrollChange` - Emitted when scroll mode changes
 * - `spreadChange` - Emitted when spread mode changes
 * - `pageModeChange` - Emitted when sidebar page mode changes
 *
 * ### User Interaction Events
 * - `onOpenFile` - Emitted when user clicks open file button
 * - `onFind` - Emitted when find/search is triggered
 * - `onUpdateFindMatchesCount` - Emitted when find matches count updates
 * - `onBookmarkClick` - Emitted when a bookmark is clicked
 * - `onAfterPrint` - Emitted after print operation completes
 *
 * ### Document Content Events
 * - `onOutlineLoaded` - Emitted when document outline/bookmarks are loaded
 * - `onAnnotationLayerRendered` - Emitted when annotation layer is rendered
 *
 * ### System Events
 * - `onIdle` - Emitted when viewer becomes idle
 *
 * @example
 * ```typescript
 * // In component template
 * <app-pdf-viewer
 *   [pdfSource]="pdfUrl"
 *   (onDocumentLoad)="handleDocumentLoad($event)"
 *   (onPageChange)="handlePageChange($event)"
 *   (onDocumentError)="handleError($event)"
 * >
 * </app-pdf-viewer>
 * ```
 *
 * @example
 * ```typescript
 * // In component class
 * onDocumentLoad(pageCount: number) {
 *   console.log(`PDF loaded with ${pageCount} pages`);
 * }
 *
 * onPageChange(pageNumber: number) {
 *   console.log(`Current page: ${pageNumber}`);
 * }
 *
 * onDocumentError(error: DocumentError) {
 *   console.error('PDF loading error:', error);
 * }
 * ```
 *
 * @since 1.0.0
 */
export interface PdfViewerOutputs {
  /**
   * Emitted when the PDF document is successfully loaded.
   *
   * The event payload contains the total number of pages in the document.
   * This is typically the first event fired after a successful PDF load.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onDocumentLoad)="handleLoad($event)"
   * // $event is the page count (number)
   * ```
   */
  onDocumentLoad?: EventEmitter<number>;

  /**
   * Emitted when the PDF document is initialized.
   *
   * Fired when the document structure is ready but before full rendering.
   * No payload is provided (void event).
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onDocumentInit)="handleInit()"
   * ```
   */
  onDocumentInit?: EventEmitter<void>;

  /**
   * Emitted when an error occurs while loading or processing the PDF document.
   *
   * The event payload contains detailed error information including error type,
   * message, and potentially stack traces for debugging.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onDocumentError)="handleError($event)"
   * // $event is DocumentError object
   * ```
   */
  onDocumentError?: EventEmitter<DocumentError>;

  /**
   * Emitted when the user navigates to a different page.
   *
   * The event payload is the new page number (1-indexed).
   * Fires on both user navigation and programmatic page changes.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onPageChange)="handlePageChange($event)"
   * // $event is the page number (number)
   * ```
   */
  onPageChange?: EventEmitter<any>;

  /**
   * Emitted when PDF pages are initialized and ready.
   *
   * The event payload contains information about all pages including
   * page count, dimensions, and other metadata.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onPagesInit)="handlePagesInit($event)"
   * // $event is PagesInfo object
   * ```
   */
  onPagesInit?: EventEmitter<PagesInfo>;

  /**
   * Emitted when the zoom/scale level changes.
   *
   * The event payload contains information about the old and new scale values.
   * Fires on both user zoom actions and programmatic zoom changes.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onScaleChange)="handleScaleChange($event)"
   * // $event is ChangedScale object with oldScale and newScale
   * ```
   */
  onScaleChange?: EventEmitter<ChangedScale>;

  /**
   * Emitted when the document rotation changes.
   *
   * The event payload contains information about the rotation change.
   * Fires on both user rotation actions and programmatic rotation.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onRotationChange)="handleRotationChange($event)"
   * // $event is ChangedRotation object
   * ```
   */
  onRotationChange?: EventEmitter<ChangedRotation>;

  /**
   * Emitted when presentation mode is toggled.
   *
   * Presentation mode is a fullscreen viewing mode optimized for presentations.
   * The event payload contains the current presentation mode state.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onPresentationModeChanged)="handlePresentationMode($event)"
   * // $event is PresentationMode object
   * ```
   */
  onPresentationModeChanged?: EventEmitter<PresentationMode>;

  /**
   * Emitted when the user clicks the "Open File" button.
   *
   * Fires when the user initiates opening a file from their local system.
   * No payload is provided (void event).
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onOpenFile)="handleOpenFile()"
   * ```
   */
  onOpenFile?: EventEmitter<void>;

  /**
   * Emitted when the find/search functionality is triggered.
   *
   * The event payload contains search-related information.
   * Fires when user initiates or interacts with the search feature.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onFind)="handleFind($event)"
   * ```
   */
  onFind?: EventEmitter<any>;

  /**
   * Emitted when the find/search matches count is updated.
   *
   * The event payload contains the current number of matches found
   * and the current match index.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onUpdateFindMatchesCount)="handleMatchesCount($event)"
   * // $event is FindMatchesCount object with matches and currentIndex
   * ```
   */
  onUpdateFindMatchesCount?: EventEmitter<FindMatchesCount>;

  /**
   * Emitted when the document outline/bookmarks are loaded.
   *
   * The event payload contains the complete document outline structure,
   * including all bookmarks and their hierarchy.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onOutlineLoaded)="handleOutline($event)"
   * // $event is DocumentOutline object
   * ```
   */
  onOutlineLoaded?: EventEmitter<DocumentOutline>;

  /**
   * Emitted when the annotation layer is rendered.
   *
   * The event payload contains information about rendered annotations.
   * Useful for tracking when interactive elements become available.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onAnnotationLayerRendered)="handleAnnotations($event)"
   * // $event is AnnotationLayerRenderEvent object
   * ```
   */
  onAnnotationLayerRendered?: EventEmitter<AnnotationLayerRenderEvent>;

  /**
   * Emitted when a bookmark in the document outline is clicked.
   *
   * The event payload contains information about the clicked bookmark,
   * including its destination and page number.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onBookmarkClick)="handleBookmarkClick($event)"
   * // $event is BookmarkClick object
   * ```
   */
  onBookmarkClick?: EventEmitter<BookmarkClick>;

  /**
   * Emitted when the viewer becomes idle (no active operations).
   *
   * Useful for tracking when the viewer has finished all rendering
   * and processing operations. No payload is provided (void event).
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onIdle)="handleIdle()"
   * ```
   */
  onIdle?: EventEmitter<void>;

  /**
   * Emitted after a print operation completes.
   *
   * Fires after the print dialog is closed or print job is sent.
   * No payload is provided (void event).
   *
   * @eventProperty
   * @example
   * ```typescript
   * (onAfterPrint)="handleAfterPrint()"
   * ```
   */
  onAfterPrint?: EventEmitter<void>;

  /**
   * Emitted when the zoom level changes.
   *
   * The event payload is the new zoom level as a string (e.g., '150%', 'page-width').
   * Alternative to `onScaleChange` with a simpler string payload.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (zoomChange)="handleZoomChange($event)"
   * // $event is the zoom level string
   * ```
   */
  zoomChange?: EventEmitter<string>;

  /**
   * Emitted when the cursor type changes.
   *
   * The event payload is the new cursor type as a string.
   * Fires when cursor mode is changed programmatically or by user interaction.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (cursorChange)="handleCursorChange($event)"
   * // $event is cursor type string ('HAND', 'SELECT', 'ZOOM')
   * ```
   */
  cursorChange?: EventEmitter<string>;

  /**
   * Emitted when the scroll mode changes.
   *
   * The event payload is the new scroll mode as a string.
   * Fires when scroll mode is changed programmatically or by user interaction.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (scrollChange)="handleScrollChange($event)"
   * // $event is scroll mode string ('VERTICAL', 'HORIZONTAL', 'WRAPPED')
   * ```
   */
  scrollChange?: EventEmitter<string>;

  /**
   * Emitted when the spread mode changes.
   *
   * The event payload is the new spread mode as a string.
   * Fires when spread mode is changed programmatically or by user interaction.
   *
   * @eventProperty
   * @example
   * ```typescript
   * (spreadChange)="handleSpreadChange($event)"
   * // $event is spread mode string ('ODD', 'EVEN', 'NONE')
   * ```
   */
  spreadChange?: EventEmitter<string>;

  /**
   * Emitted when the sidebar page mode changes.
   *
   * The event payload is the new page mode as a string.
   * Fires when sidebar mode is changed (e.g., switching from thumbnails to bookmarks).
   *
   * @eventProperty
   * @example
   * ```typescript
   * (pageModeChange)="handlePageModeChange($event)"
   * // $event is page mode string ('none', 'thumbs', 'bookmarks', 'attachments')
   * ```
   */
  pageModeChange?: EventEmitter<string>;
}
