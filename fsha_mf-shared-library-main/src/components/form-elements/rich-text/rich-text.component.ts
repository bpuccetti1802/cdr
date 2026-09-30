import {
  CUSTOM_ELEMENTS_SCHEMA,
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges,
  ViewEncapsulation,
} from '@angular/core';
import {
  ContentChange,
  EditorChangeContent,
  EditorChangeSelection,
  QuillEditorComponent,
} from 'ngx-quill';
import Quill from 'quill';
import { FormsModule } from '@angular/forms';
import type { ClassAttributor, StyleAttributor } from 'parchment';

/* CONFIGURAZIONE QUILL */
// Importante: prendere Block dal registry dell'istanza Quill CONDIVISA (singleton del module
// federation) con Quill.import, NON con `import Block from 'quill/blots/block'`. Quel deep import
// verrebbe bundlato a parte creando un secondo registry Parchment: i blot finirebbero in registry
// diversi e l'optimize andrebbe in loop ("Maximum optimize iterations reached") in build di prod.
const Block = Quill.import('blots/block') as typeof import('quill/blots/block').default;
Block.tagName = 'DIV';
Quill.register(Block, true);

// Font whitelist
const Font = Quill.import('formats/font') as ClassAttributor;
Font.whitelist = ['arial', 'times-new-roman', 'calibri', 'georgia', 'courier-new'];
Quill.register(Font, true);

// Font size whitelist
const SizeStyle = Quill.import('attributors/style/size') as StyleAttributor;
SizeStyle.whitelist = ['10px', '12px', '14px', '16px', '18px', '24px', '32px'];
Quill.register(SizeStyle, true);

export interface RichTextChange {
  deltaJson: string;
  html: string;
}

@Component({
  imports: [QuillEditorComponent, FormsModule],
  selector: 'app-rc-rich-text',
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  standalone: true,
  templateUrl: './rich-text.component.html',
  styleUrls: ['./rich-text.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class RichTextComponent implements OnChanges {
  @Output() dataChange = new EventEmitter<RichTextChange>();
  @Input() label!: string;
  @Input() placeholder!: string;
  @Input() text!: string;
  @Input() readOnly: boolean = false;
  blurred = false;
  focused = false;

  quill!: Quill;

  editorModules = {
    toolbar: {
      container: [
        ['undo', 'redo'],
        [{ font: ['arial', 'times-new-roman', 'calibri', 'georgia', 'courier-new'] }],
        [{ size: ['10px', '12px', '14px', '16px', '18px', '24px', '32px'] }],
        [{ header: [1, 2, 3, false] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ color: [] }, { background: [] }],
        [{ align: [] }],
        [{ list: 'ordered' }, { list: 'bullet' }],
        [{ indent: '-1' }, { indent: '+1' }],
        ['link', 'image'],
      ],
      handlers: {
        undo: () => this.quill?.history.undo(),
        redo: () => this.quill?.history.redo(),
      },
    },
    history: {
      delay: 1000,
      maxStack: 200,
      userOnly: true,
    },
  };

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['text'] && this.quill && this.text) {
      this.setJsonContent();
    }
  }

  /**
   * Metodo in ascolto dell'evento di creazione dell'editor di Quill.
   * Alla creazione salva l'istanza corrente di Quill e precarica il testo se presente
   * @param event The quill editor instance.
   */
  onEditorCreated(event: Quill) {
    this.quill = event;

    if (this.text) this.setJsonContent();
  }

  /**
   * Metodo in ascolto dei cambiamenti nell'editor di Quill
   * @param event
   */
  changedEditor(event: EditorChangeContent | EditorChangeSelection) {}

  /**
   * Metodo in ascolto dei cambiamenti del testo nell'editor di Quill.
   * Alla modifica converte il contenuto in JSON e in HTML e li emette
   * @param event
   * @returns
   */
  onContentChanged(event: ContentChange) {
    if (!event?.editor) return;

    const fullDelta = event.editor.getContents();
    const deltaJson = JSON.stringify(fullDelta);

    const html = event.editor.root.innerHTML; // per anteprima iframe e stampa

    this.dataChange.emit({ deltaJson, html });
  }

  focus($event: Event) {
    this.focused = true;
    this.blurred = false;
  }

  nativeFocus($event: Event) {}

  blur($event: Event) {
    this.focused = false;
    this.blurred = true;
  }
  nativeBlur($event: Event) {}

  /**
   * Metodo che si occupa di precompilare il testo nell'editor di Quill.
   * Controlla se il testo è un JSON di tipo Delta e lo inserisce come contenuto.
   * Altrimenti tratta il testo come HTML: lo converte in Delta JSON con
   * `htmlToDeltaJson` e aggiorna lo stato dell'editor con `setContents`.
   * @returns
   */
  private setJsonContent() {
    if (!this.quill || !this.text) {
      return;
    }

    try {
      const parsed = JSON.parse(this.text);

      // verifico che il JSON parsato sia di tipo Delta
      if (parsed && typeof parsed === 'object' && Array.isArray(parsed.ops)) {
        this.quill.setContents(parsed);
      } else {
        // JSON valido ma non di tipo Delta: lo tratto come HTML/testo
        this.setHtmlContent(this.text);
      }
    } catch {
      // non è JSON quindi lo tratto come HTML/testo
      this.setHtmlContent(this.text);
    }
  }

  /**
   * Converte una stringa HTML nel Delta JSON tramite `htmlToDeltaJson` e aggiorna
   * lo stato dell'editor con `setContents`, così l'HTML viene renderizzato come
   * contenuto formattato invece di essere mostrato come testo grezzo.
   * @param {string} html Stringa HTML da renderizzare.
   * @returns {void}
   */
  private setHtmlContent(html: string): void {
    const deltaJson = this.htmlToDeltaJson(html);
    if (deltaJson) {
      this.quill.setContents(JSON.parse(deltaJson));
    }
  }

  /**
   * Converte una stringa HTML nel corrispondente Delta JSON di Quill.
   * Utile per trasformare il `text` (HTML) nel formato Delta serializzato,
   * compatibile con `setContents` e con il `deltaJson` emesso da `dataChange`.
   *
   * @param {string} html Stringa HTML da convertire.
   * @returns {string} Il Delta serializzato in JSON (stringa vuota se l'editor non è pronto o l'input è vuoto).
   */
  htmlToDeltaJson(html: string): string {
    if (!this.quill || !html) {
      return '';
    }

    const delta = this.quill.clipboard.convert({ html });
    return JSON.stringify(delta);
  }
}
