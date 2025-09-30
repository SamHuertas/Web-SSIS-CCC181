export class ProgramValidator {
  
  // Format program code to uppercase
  formatProgramCode(code) {
    if (!code) return '';
    return String(code).trim().toUpperCase();
  }

  // Format program name to title case
  formatProgramName(name) {
    if (!name) return '';
    return String(name).trim().toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
  }

  // Validate program code
  validateProgramCode(code) {
    if (!code || !code.trim()) {
      return { isValid: false, error: 'Program code is required' };
    }

    const cleanCode = code.trim();

    if (cleanCode.length < 2 || cleanCode.length > 10) {
      return { isValid: false, error: 'Program code must be between 2 and 10 characters' };
    }

    // Only allow letters
    if (!/^[A-Za-z]+$/.test(cleanCode)) {
      return { isValid: false, error: 'Program code can only contain letters' };
    }

    return { isValid: true, error: null };
  }

  // Validate program name
  validateProgramName(name) {
    if (!name || !name.trim()) {
      return { isValid: false, error: 'Program name is required' };
    }

    const cleanName = name.trim();

    if (cleanName.length < 3 || cleanName.length > 100) {
      return { isValid: false, error: 'Program name must be between 3 and 100 characters' };
    }

    // Only allow letters, spaces, and hyphens
    if (!/^[A-Za-z\s\-,()]+$/.test(cleanName)) {
      return { isValid: false, error: 'Program name can only contain letters, spaces, commas, parenthesis and hyphens' };
    }

    return { isValid: true, error: null };
  }

  // Validate and format program data
  validateAndFormatProgram(programData) {
    const { program_code, program_name, college_code } = programData;

    const codeValidation = this.validateProgramCode(program_code);
    if (!codeValidation.isValid) {
      return { isValid: false, error: codeValidation.error, formattedData: null };
    }

    const nameValidation = this.validateProgramName(program_name);
    if (!nameValidation.isValid) {
      return { isValid: false, error: nameValidation.error, formattedData: null };
    }

    const formattedData = {
      program_code: this.formatProgramCode(program_code),
      program_name: this.formatProgramName(program_name),
      college_code: college_code.trim()
    };

    return { isValid: true, error: null, formattedData };
  }
}

export default new ProgramValidator();