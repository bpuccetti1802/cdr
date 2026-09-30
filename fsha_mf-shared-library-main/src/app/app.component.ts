import { Component, Type } from '@angular/core';
import { CardWrapperComponent } from '../components/card-wrapper/card-wrapper.component';
import { TableComponent } from '@mf/components/table/table.component';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { DateTime } from 'luxon';
import { OtpComponent } from './../components/form-elements/otp/otp.component';
import { QuillConfigModule, QuillModule } from 'ngx-quill';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ReactiveFormsModule, OtpComponent, QuillConfigModule, QuillModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'mf-shared-library';
  breadcrumbs = [{ label: 'Home', url: '/' }, { label: 'Event Manager' }];
  tabs: {
    label: string;
    iconName?: string;
    iconColor?: string;
    component: Type<unknown>;
  }[] = [
    {
      label: 'Dashboard',
      iconName: 'it-check-circle',
      iconColor: 'success',
      component: CardWrapperComponent,
    },
    {
      label: 'Amministrazione',
      iconName: 'it-check-circle',
      iconColor: 'success',
      component: CardWrapperComponent,
    },
    {
      label: 'Dati Personali',
      iconName: 'it-info-circle',
      iconColor: 'secondary',
      component: CardWrapperComponent,
    },
    {
      label: 'Gestione Password',
      iconName: 'it-info-circle',
      iconColor: 'secondary',
      component: CardWrapperComponent,
    },
    {
      label: 'Amministrazione Trasparente',
      iconName: 'it-info-circle',
      iconColor: 'secondary',
      component: CardWrapperComponent,
    },
    {
      label: 'Applicativi',
      iconName: 'it-info-circle',
      iconColor: 'secondary',
      component: CardWrapperComponent,
    },
    {
      label: 'Servizi',
      iconName: 'it-info-circle',
      iconColor: 'secondary',
      component: CardWrapperComponent,
    },
    {
      label: 'Documentazione',
      iconName: 'it-info-circle',
      iconColor: 'secondary',
      component: CardWrapperComponent,
    },
    {
      label: 'Gestione Pratiche',
      iconName: 'it-info-circle',
      iconColor: 'secondary',
      component: CardWrapperComponent,
    },
  ];

  contentComponent = TableComponent;

  form = new FormGroup({
    selectedDate: new FormControl<DateTime | null>(DateTime.now()), // inizializzazione con null o un valore specifico
  });
  Test: string = 'label';
  codiceOtp: string = '';

  constructor() {}

  salvaCodiceOtp(codice: string) {
    this.codiceOtp = codice;
    console.log('TEST', codice);
  }

  stampaOtp() {
    console.log('Stampa OTP:', this.codiceOtp);
  }
}
