// AGGRESSIVE German word correction for PP-OCRv5
// Tries to fix common OCR failures for German text

#ifndef GERMAN_WORD_CORRECTION_AGGRESSIVE_H
#define GERMAN_WORD_CORRECTION_AGGRESSIVE_H

#include <string>
#include <unordered_map>
#include <algorithm>
#include <cctype>

// Aggressive German word corrections
static std::string correctGermanTextAggressive(const std::string& text) {
    if (text.empty()) return text;
    
    std::string result = text;
    
    // COMMON GERMAN OCR FAILURES (based on actual testing)
    // Format: {what_OCR_recognizes, what_it_should_be}
    const std::unordered_map<std::string, std::string> CORRECTIONS = {
        // Umlauts completely missing
        {"FR", "FÜR"},
        {"FUR", "FÜR"},
        {"F R", "FÜR"},
        
        {"SCHN", "SCHÖN"},
        {"SCHON", "SCHÖN"},
        {"SCH N", "SCHÖN"},
        {"5CHON", "SCHÖN"},  // 5 looks like S
        
        {"RGER", "ÄRGER"},
        {"ARGER", "ÄRGER"},
        {"R GER", "ÄRGER"},
        
        {"GRO", "GROß"},
        {"GROS", "GROß"},
        {"GRO SS", "GROß"},
        
        // Common German words with Umlauts
        {"HAUSER", "HÄUSER"},
        {"HAUSer", "Häuser"},
        {"HAUSE", "HÄUSER"},
        
        {"STRASE", "STRASSE"},
        {"STRASSE", "STRAßE"},  // Note: ß vs SS
        {"STRAS E", "STRAßE"},
        
        {"MUNCHEN", "MÜNCHEN"},
        {"MU NCHEN", "MÜNCHEN"},
        
        {"UBER", "ÜBER"},
        {"U BER", "ÜBER"},
        
        // Number/letter confusions (common in OCR)
        {"5", "S"},
        {"0", "O"},
        {"1", "I"},
        {"8", "B"},
        
        // Letter combinations that look like other letters
        {"rn", "m"},
        {"cl", "d"},
        {"vv", "w"},
        {"ii", "u"},
    };
    
    // Apply ALL corrections (aggressive mode)
    for (const auto& correction : CORRECTIONS) {
        size_t pos = 0;
        while ((pos = result.find(correction.first, pos)) != std::string::npos) {
            // Always replace in aggressive mode
            result.replace(pos, correction.first.length(), correction.second);
            pos += correction.second.length();
        }
    }
    
    // SPECIAL CASE: "SCHN" → "SCHÖN" (even if not exact match)
    // Sometimes OCR gives "5CHN", "5CHON", etc.
    if (result.find("CHN") != std::string::npos || 
        result.find("CHON") != std::string::npos) {
        // Check if it looks like "SCHÖN" variant
        size_t pos = result.find("CHN");
        if (pos != std::string::npos && pos >= 2) {
            // Check for S/5 at beginning
            if (result[pos-2] == 'S' || result[pos-2] == '5') {
                if (result[pos-1] == 'C' || result[pos-1] == 'G') {  // C/G confusion
                    result.replace(pos-2, 5, "SCHÖN");
                }
            }
        }
    }
    
    // SPECIAL CASE: "FR" → "FÜR"
    if (result == "FR" || result.find(" FR ") != std::string::npos) {
        size_t pos = result.find("FR");
        if (pos != std::string::npos) {
            result.replace(pos, 2, "FÜR");
        }
    }
    
    // SPECIAL CASE: "RGER" → "ÄRGER"  
    if (result.find("RGER") != std::string::npos) {
        size_t pos = result.find("RGER");
        if (pos != std::string::npos) {
            // Check if it's at start or after space
            if (pos == 0 || !std::isalpha(result[pos-1])) {
                result.replace(pos, 4, "ÄRGER");
            }
        }
    }
    
    return result;
}

#endif // GERMAN_WORD_CORRECTION_AGGRESSIVE_H