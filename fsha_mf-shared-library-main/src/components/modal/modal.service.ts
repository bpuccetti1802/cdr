import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ModalService {
  private closeModalSubject = new Subject<void>();

  // Observable per sottoscrivere eventi di chiusura del modal
  getTriggersEvents() {
    return this.closeModalSubject.asObservable();
  }

  // Metodo per triggerare la chiusura del modal
  triggerCloseModal() {
    this.closeModalSubject.next(); // Emesso l'evento
  }
}
