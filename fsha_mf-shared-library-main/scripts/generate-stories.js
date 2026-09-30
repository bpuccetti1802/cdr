const fs = require('fs');
const path = require('path');

// Directory dei componenti e delle storie
const componentsDir = path.join(__dirname, '../src/components');
const storyDir = path.join(__dirname, '../src/stories');

// Controllo delle directory
console.log('Directory dei componenti:', componentsDir);
console.log('Directory delle storie:', storyDir);

if (!fs.existsSync(componentsDir)) {
  console.error(`Errore: La directory dei componenti non esiste: ${componentsDir}`);
  process.exit(1);
}

if (!fs.existsSync(storyDir)) {
  console.warn(`Avviso: La directory delle storie non esiste. La sto creando...`);
  fs.mkdirSync(storyDir, { recursive: true });
}

// Funzione per leggere il nome della classe e gli input dal file del componente
function analyzeComponent(filePath) {
  const fileContent = fs.readFileSync(filePath, 'utf8');
  
  // Trova il nome della classe
  const classMatch = fileContent.match(/export\s+class\s+(\w+)\s+/);
  const className = classMatch ? classMatch[1] : null;

  // Trova le proprietà annotate con @Input
  const inputs = [];
  const inputRegex = /@Input(?:\(\s*['"`]?(.*?)['"`]?\s*\))?\s*(?:public|private|protected)?\s*(\w+)/g;
  let match;

  while ((match = inputRegex.exec(fileContent)) !== null) {
    const inputName = match[1] || match[2]; // Usa il nome personalizzato o il nome della proprietà
    inputs.push(inputName);
  }

  return { className, inputs };
}

// Funzione per generare una story base
function generateStory(componentName, componentPath, inputs) {
  const importPath = componentPath.replace(/\\/g, '/'); // Corregge i separatori di percorso su Windows
  const args = inputs
    .map(input => `    ${input}: 'example ${input}'`)
    .join(',\n');
  return `import type { Meta, StoryObj } from '@storybook/angular';
import { ${componentName} } from '${importPath}';

const meta: Meta<${componentName}> = {
  title: 'Components/${componentName}',
  component: ${componentName},
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<${componentName}>;

export const Primary: Story = {
  name: 'Default',
  args: {
${args}
  },
};
  `;
}

// Generazione delle storie
fs.readdirSync(componentsDir, { withFileTypes: true })
  .filter(dirent => dirent.isDirectory()) // Considera solo le directory
  .forEach(componentFolder => {
    const componentName = componentFolder.name;
    const componentFilePath = path.join(
      componentsDir,
      componentName,
      `${componentName}.component.ts`
    );

    if (!fs.existsSync(componentFilePath)) {
      console.warn(`Avviso: File componente non trovato per ${componentName}`);
      return;
    }

    const { className, inputs } = analyzeComponent(componentFilePath);

    if (!className) {
      console.warn(`Avviso: Nome della classe non trovato per ${componentName}`);
      return;
    }

    const relativeComponentPath = path.relative(
      path.join(storyDir),
      componentFilePath.replace(/\.ts$/, '')
    );

    const storyContent = generateStory(className, relativeComponentPath, inputs);
    const storyPath = path.join(storyDir, `${className}.stories.ts`);
    fs.writeFileSync(storyPath, storyContent);
    console.log(`Story generata per il componente: ${className}`);
  });
