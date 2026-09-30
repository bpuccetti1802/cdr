const {
  shareAll,
  withModuleFederationPlugin,
} = require('@angular-architects/module-federation/webpack');

module.exports = {
  ...withModuleFederationPlugin({
    name: 'mfSharedLibrary',
    filename: 'remoteEntry.js',
    exposes: {
      './GlobalErrorHandler': './src/core/error/global-error.handler.ts',
      './EventBus': './src/core/event-bus/event-bus.ts',
      // Interceptors
      './AuthenticationInterceptor': './src/core/http/interceptors/authentication.interceptor.ts',
      './HttpErrorInterceptor': './src/core/http/interceptors/http-error.interceptor.ts',
      './HttpLoadingInterceptor': './src/core/http/interceptors/http-loading.interceptor.ts',
      // Services
      './LoadStruttureListService': './src/services/strutture-list/load-strutture-list.service.ts',
      './ConfigService': './src/services/configuration/dynamic-config.service.ts',
      './BaseHrefService': './src/services/base-href/base-href.service.ts',
      './NavigationFragmentService':
        './src/services/navigation-fragments/navigation-fragment.service.ts',
      './ObjectExtensionsService':
        './src/core/utils/object-extensions/object-extensions.service.ts',
      './AbilityService': './src/services/abilitation/abilitation.service.ts',
      './AuthorizationService': './src/services/authorization/authorization.service.ts',
      './BaseAuthorizationGuard': './src/services/authorization/base-authorization.guard.ts',
      './AuthorizationGuard': './src/services/authorization/authorization.guard.ts',
      './ResponsiveService': './src/services/responsive/responsive.service.ts',
      './HttpLoadingService': './src/core/http/loading/http-loading.service.ts',
      './LocalStorageService': './src/services/local-storage/local-storage.service.ts',
      './AuthenticationService': './src/services/authentication/authentication.service.ts',
      './TipoIstanzaService': './src/services/tipo-istanza/tipo-istanza.service.ts',
      './AuthenticationGuard': './src/services/authentication/authentication.guard.ts',
      './AuthenticationIAMGuard': './src/services/authentication-iam/authentication-iam.guard.ts',
      './HttpClientService': './src/core/http/client/http-client.service.ts',
      './InjectionTokenService': './src/core/token/injection-token.service.ts',
      // Components
      './PdfViewerComponent': './src/components/pdf-viewer/pdf-viewer.component.ts',
      './ToggleIconComponent': './src/components/toggle-icon/toggle-icon.component.ts',
      './SidebarComponent': './src/components/sidebar/sidebar.component.ts',
      './DoughnutChartComponent': './src/components/charts/doughnut/doughnut-chart.component.ts',
      './NotificationContainerComponent':
        './src/components/notification-container/notification-container.component.ts',
      './ImageComponent': './src/components/image/image.component.ts',
      './BadgeComponent': './src/components/badge/badge.component.ts',
      './Component': './src/app/app.component.ts',
      './BreadcrumbComponent': './src/components/breadcrumb/breadcrumb.component.ts',
      './Breadcrumb': './src/components/breadcrumb/breadcrumb.module.ts',
      './LayoutRouterOutletComponent':
        './src/components/layout-router-outlet/layout-router-outlet.component.ts',
      './HeaderComponent': './src/components/header/header.component.ts',
      './NavbarComponent': './src/components/navbar/navbar.component.ts',
      './FooterComponent': './src/components/footer/footer.component.ts',
      './MenuComponent': './src/components/menu/menu.component.ts',
      './TabsVerticalComponent': './src/components/tabs-vertical/tabs-vertical.component.ts',
      './TabsVertical': './src/components/tabs-vertical/tabs-vertical.module.ts',
      './TabsHorizontalComponent': './src/components/tabs-horizontal/tabs-horizontal.component.ts',
      './TabsHorizontalVersion2Component':
        './src/components/tabs-horizontal-v2/tabs-horizontal-v2.component.ts',
      './TabsHorizontal': './src/components/tabs-horizontal/tabs-horizontal.module.ts',
      './CarouselComponent': './src/components/carousel/carousel.component.ts',
      './CardWrapperComponent': './src/components/card-wrapper/card-wrapper.component.ts',
      './CardWrapper': './src/components/card-wrapper/card-wrapper.module.ts',
      './CheckboxTableComponent': './src/components/checkbox-table/checkbox-table.component.ts',
      './CheckboxTableModule': './src/components/checkbox-table/checkbox-table.module.ts',
      './TableComponent': './src/components/table/table.component.ts',
      './RichTextComponent': './src/components/form-elements/rich-text/rich-text.component.ts',
      './Table': './src/components/table/table.module.ts',
      './TableToolbarComponent': './src/components/table-toolbar/table-toolbar.component.ts',
      './IconComponent': './src/components/icon/icon.component.ts',
      './ModalComponent': './src/components/modal/modal.component.ts',
      './InputComponent': './src/components/form-elements/input/input.component.ts',
      './Input': './src/components/form-elements/input/input.module.ts',
      './TextAreaComponent': './src/components/form-elements/textarea/textarea.component.ts',
      './NotificationToastComponent':
        './src/components/notification-toast/notification-toast.component.ts',
      './NotificationToast': './src/components/notification-toast/notification-toast.module.ts',
      './InputPasswordComponent':
        './src/components/form-elements/input-password/input-password.component.ts',
      './InputPassword': './src/components/form-elements/input-password/input-password.module.ts',
      './SelectAutocompleteComponent':
        './src/components/form-elements/select-autocomplete/select-autocomplete.component.ts',
      './MultiSelectAutoaddComponent':
        './src/components/form-elements/multi-select-autoadd/multi-select-autoadd.component.ts',
      './PickerComponent': './src/components/form-elements/picker/picker.component.ts',
      './CheckboxComponent': './src/components/form-elements/checkbox/checkbox.component.ts',
      './Checkbox': './src/components/form-elements/checkbox/checkbox.module.ts',
      './ButtonIconComponent': './src/components/button-icon/button-icon.component.ts',
      './DateTimePickerComponent':
        './src/components/form-elements/datetime-picker/datetime-picker.component.ts',
      './DateTimePicker':
        './src/components/form-elements/datetime-picker/datetime-picker.module.ts',
      './UploadComponent': './src/components/form-elements/upload/upload.component.ts',
      './AccordionComponent': './src/components/accordion/accordion.component.ts',
      './Accordion': './src/components/accordion/accordion.module.ts',
      './SpinnerComponent': './src/components/spinner/spinner.component.ts',
      './Spinner': './src/components/spinner/spinner.module.ts',
      './SelectComponent': './src/components/form-elements/select/select.component.ts',
      './Select2VersionComponent':
        './src/components/form-elements/select-2v/select-2v.component.ts',
      './Select2Version': './src/components/form-elements/select-2v/select-2v.module.ts',
      './Select': './src/components/form-elements/select/select.module.ts',
      './FileNotFoundComponent': './src/components/file-not-found/file-not-found.component.ts',
      './FileNotFound': './src/components/file-not-found/file-not-found.module.ts',
      './ErrorBoundaryComponent': './src/components/error-boundary/error-boundary.component.ts',
      './ErrorBoundary': './src/components/error-boundary/error-boundary.module.ts',
      './NavigationButtonComponent':
        './src/components/navigation-button/navigation-button.component.ts',
      './RadioComponent': './src/components/form-elements/radio/radio.component.ts',
      './StepperComponent': './src/components/stepper/stepper.component.ts',
      './InputNumberComponent':
        './src/components/form-elements/input-number/input-number.component.ts',
      './DatePickerComponent':
        './src/components/form-elements/date-picker/date-picker.component.ts',
      './DateRangePickerComponent':
        './src/components/form-elements/daterange-picker/daterange-picker.component.ts',
      './DocumentSingleUploadComponent':
        './src/components/form-elements/document-single-upload/document-single-upload.component.ts',
      './ButtonComponent': './src/components/button/button.component.ts',
      './DocumentSingleUploadComponent':
        './src/components/form-elements/document-single-upload/document-single-upload.component.ts',
      './GridComponent': './src/components/grid/grid.component.ts',
      './OtpComponent': './src/components/form-elements/otp/otp.component.ts',
      './Otp': './src/components/form-elements/otp/otp.module.ts',
      './MapComponent': './src/components/map/map.component.ts',
      './ItUploadDragDropComponent':
        './src/components/upload-drag-drop/upload-drag-drop.component.ts',
      './StackedBarChartComponent':
        './src/components/charts/stacked-bar-chart/stacked-bar-chart.component.ts',
      './UnderConstructionComponent':
        './src/components/under-construction/under-construction.component.ts',
      './TimePickerComponent':
        './src/components/form-elements/time-picker/time-picker.component.ts',
      './TimeRangePickerComponent':
        './src/components/form-elements/timerange-picker/timerange-picker.component.ts',
    },
    shared: {
      ...shareAll({ singleton: true, strictVersion: true, requiredVersion: 'auto' }),
      'test-library-frankmd93': { singleton: false, strictVersion: false },
      'ng2-pdfjs-viewer': { singleton: false, strictVersion: false },
    },
  }),
};
