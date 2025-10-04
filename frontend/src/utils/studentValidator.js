export class StudentValidator {
    //Format ID number to XXXX-XXXX format
    formatIdNumber(idNumber) {
    if (!idNumber) return '';
    // Remove any existing hyphens and spaces
    const cleaned = String(idNumber).replace(/[\s\-]/g, '');
    // Insert hyphen after 4th digit
    if (cleaned.length === 8) {
      return `${cleaned.substring(0, 4)}-${cleaned.substring(4)}`;
    }
    return cleaned;
  }

  // Format name to title case
  formatName(name) {
    if (!name) return '';
    return String(name).trim().toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
  }

  // Validate ID number
  validateIdNumber(idNumber) {
    if (!idNumber || !String(idNumber).trim()) {
      return { isValid: false, error: 'ID number is required' };
    }

    const cleaned = String(idNumber).replace(/[\s\-]/g, '').trim();

    // Must be exactly 8 digits
    if (cleaned.length !== 8) {
      return { isValid: false, error: 'ID number must be exactly 8 digits (format: XXXX-XXXX)' };
    }

    // Only allow digits
    if (!/^\d{8}$/.test(cleaned)) {
      return { isValid: false, error: 'ID number can only contain digits' };
    }

    return { isValid: true, error: null };
  }

  // Validate first name
  validateFirstName(firstName) {
    if (!firstName || !firstName.trim()) {
      return { isValid: false, error: 'First name is required' };
    }

    const cleanName = firstName.trim();

    if (cleanName.length < 2 || cleanName.length > 50) {
      return { isValid: false, error: 'First name must be between 2 and 50 characters' };
    }

    // Only allow letters, spaces, and hyphens
    if (!/^[A-Za-z\s\-]+$/.test(cleanName)) {
      return { isValid: false, error: 'First name can only contain letters, spaces, and hyphens' };
    }

    return { isValid: true, error: null };
  }

  // Validate last name
  validateLastName(lastName) {
    if (!lastName || !lastName.trim()) {
      return { isValid: false, error: 'Last name is required' };
    }

    const cleanName = lastName.trim();

    if (cleanName.length < 2 || cleanName.length > 50) {
      return { isValid: false, error: 'Last name must be between 2 and 50 characters' };
    }

    // Only allow letters and spaces
    if (!/^[A-Za-z\s]+$/.test(cleanName)) {
      return { isValid: false, error: 'Last name can only contain letters and spaces' };
    }

    return { isValid: true, error: null };
  }

  validateAndFormatStudent(studentData) {
    const { id_number, first_name, last_name, year_level, gender, program_code } = studentData;

    // Format and validate each field
    const IdValidation = this.validateIdNumber(id_number);
    if(!IdValidation.isValid){
        return { isValid: false, error: IdValidation.error, formattedData: null };
    }

    const firstNameValidation = this.validateFirstName(first_name);
    if (!firstNameValidation.isValid) {
      return { isValid: false, error: firstNameValidation.error, formattedData: null };
    }

    const lastNameValidation = this.validateLastName(last_name);
    if (!lastNameValidation.isValid) {
      return { isValid: false, error: lastNameValidation.error, formattedData: null };
    }

    const formattedData = {
        id_number: this.formatIdNumber(id_number),
        first_name: this.formatName(first_name),
        last_name: this.formatName(last_name),
        year_level: year_level.trim(),
        gender: gender.trim(),
        program_code: program_code.trim()
    };

    return { isValid: true, error: null, formattedData };
  }
}

export default new StudentValidator();