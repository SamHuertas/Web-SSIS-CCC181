export class CollegeValidator {
  
  // Format college code to uppercase
  formatCollegeCode(code) {
    if (!code) return '';
    return String(code).trim().toUpperCase();
  }

  // Format college name to title case
  formatCollegeName(name) {
    if (!name) return '';
    return String(name).trim().toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
  }

  // Validate college code
  validateCollegeCode(code) {
    if (!code || !code.trim()) {
      return { isValid: false, error: 'College code is required' };
    }

    const cleanCode = code.trim();

    if (cleanCode.length < 2 || cleanCode.length > 10) {
      return { isValid: false, error: 'College code must be between 2 and 10 characters' };
    }

    // Only allow letters
    if (!/^[A-Za-z]+$/.test(cleanCode)) {
      return { isValid: false, error: 'College code can only contain letters' };
    }

    return { isValid: true, error: null };
  }

  // Validate college name
  validateCollegeName(name) {
    if (!name || !name.trim()) {
      return { isValid: false, error: 'College name is required' };
    }

    const cleanName = name.trim();

    if (cleanName.length < 3 || cleanName.length > 100) {
      return { isValid: false, error: 'College name must be between 3 and 100 characters' };
    }

    // Only allow letters, spaces, and hyphens
    if (!/^[A-Za-z\s\-,]+$/.test(cleanName)) {
      return { isValid: false, error: 'College name can only contain letters, spaces, commas, and hyphens' };
    }

    return { isValid: true, error: null };
  }

  // Validate and format college data
  validateAndFormatCollege(collegeData) {
    const { college_code, college_name } = collegeData;

    const codeValidation = this.validateCollegeCode(college_code);
    if (!codeValidation.isValid) {
      return { isValid: false, error: codeValidation.error, formattedData: null };
    }

    const nameValidation = this.validateCollegeName(college_name);
    if (!nameValidation.isValid) {
      return { isValid: false, error: nameValidation.error, formattedData: null };
    }

    const formattedData = {
      college_code: this.formatCollegeCode(college_code),
      college_name: this.formatCollegeName(college_name)
    };

    return { isValid: true, error: null, formattedData };
  }
}

export default new CollegeValidator();