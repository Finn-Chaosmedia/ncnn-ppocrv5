// German word correction for PP-OCRv5
// Improves recognition of German words with umlauts and special characters
// Includes basic European character correction

#ifndef GERMAN_WORD_CORRECTION_H
#define GERMAN_WORD_CORRECTION_H

#include <string>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <cctype>

// Basic European character corrections (common OCR misrecognitions)
static std::string correctEuropeanCharacters(const std::string& input) {
    std::string result = input;
    
    // Common OCR misrecognitions for European characters
    const std::unordered_map<std::string, std::string> CHAR_CORRECTIONS = {
        // Numbers vs Letters
        {"0", "O"}, {"O", "0"},  // Zero vs Oh
        {"1", "I"}, {"I", "1"},  // One vs Eye
        {"5", "S"}, {"S", "5"},  // Five vs Ess
        {"8", "B"}, {"B", "8"},  // Eight vs Bee
        
        // Common letter combinations that look like other letters
        {"rn", "m"}, {"cl", "d"}, {"vv", "w"},
        {"ii", "u"}, {"nn", "m"}, {"ci", "a"}
    };
    
    // Apply character corrections
    for (const auto& correction : CHAR_CORRECTIONS) {
        size_t pos = 0;
        while ((pos = result.find(correction.first, pos)) != std::string::npos) {
            result.replace(pos, correction.first.length(), correction.second);
            pos += correction.second.length();
        }
    }
    
    return result;
}

// Common German words that often get misrecognized by Chinese-trained OCR
static const std::unordered_map<std::string, std::string> GERMAN_WORD_CORRECTIONS = {
    // Umlaut problems
    {"schn", "schön"},
    {"schon", "schön"},
    {"schone", "schöne"},
    {"schones", "schönes"},
    
    {"Huser", "Häuser"},
    {"Hauser", "Häuser"},
    {"Hause", "Häuse"},
    
    {"strae", "straße"},
    {"strase", "straße"},
    {"Strae", "Straße"},
    
    {"Munchen", "München"},
    {"Muchen", "München"},
    
    {"uber", "über"},
    {"Uber", "Über"},
    
    {"ofen", "öfen"},
    {"Ofen", "Öfen"},
    
    // Common German words (frequent OCR errors)
    {"und", "und"},
    {"der", "der"},
    {"die", "die"},
    {"das", "das"},
    {"ein", "ein"},
    {"eine", "eine"},
    {"ich", "ich"},
    {"du", "du"},
    {"wir", "wir"},
    {"sie", "sie"},
    {"er", "er"},
    {"es", "es"},
    
    // Word endings often misrecognized
    {"ung", "ung"},
    {"heit", "heit"},
    {"keit", "keit"},
    {"schaft", "schaft"},
    {"chen", "chen"},
    {"lein", "lein"},
    
    // Common letter confusions in German
    {"rn", "m"},      // "rn" looks like "m"
    {"cl", "d"},      // "cl" looks like "d"
    {"vv", "w"},      // "vv" looks like "w"
    {"ii", "u"},      // "ii" looks like "u" (cursive)
};

// Check if a word looks German (contains typical German patterns)
static bool looksLikeGermanWord(const std::string& word) {
    if (word.empty()) return false;
    
    // Check for German umlauts (if they survived OCR)
    if (word.find("a") != std::string::npos ||
        word.find("o") != std::string::npos ||
        word.find("u") != std::string::npos ||
        word.find("A") != std::string::npos ||
        word.find("O") != std::string::npos ||
        word.find("U") != std::string::npos ||
        word.find("ss") != std::string::npos) {
        return true;
    }
    
    // Check for common German word endings
    std::string lowerWord = word;
    std::transform(lowerWord.begin(), lowerWord.end(), lowerWord.begin(), ::tolower);
    
    const std::vector<std::string> germanEndings = {
        "ung", "heit", "keit", "schaft", "chen", "lein", "ig", "lich", "sam", "bar"
    };
    
    for (const auto& ending : germanEndings) {
        if (lowerWord.length() >= ending.length() &&
            lowerWord.substr(lowerWord.length() - ending.length()) == ending) {
            return true;
        }
    }
    
    // Check if word is in correction dictionary
    return GERMAN_WORD_CORRECTIONS.find(lowerWord) != GERMAN_WORD_CORRECTIONS.end();
}

// Apply German word correction
static std::string correctGermanWord(const std::string& word) {
    if (word.empty()) return word;
    
    std::string lowerWord = word;
    std::transform(lowerWord.begin(), lowerWord.end(), lowerWord.begin(), ::tolower);
    
    // First check exact match in correction dictionary
    auto it = GERMAN_WORD_CORRECTIONS.find(lowerWord);
    if (it != GERMAN_WORD_CORRECTIONS.end()) {
        return it->second;
    }
    
    // If no exact match, try to apply character-level corrections
    // (This is a simple implementation - could be expanded)
    std::string result = word;
    
    // Common OCR errors for German
    if (result.find("schon") != std::string::npos) {
        size_t pos = result.find("schon");
        if (pos != std::string::npos && (pos + 5 == result.length() || !std::isalpha(result[pos + 5]))) {
            result.replace(pos, 5, "schön");
        }
    }
    
    if (result.find("Hauser") != std::string::npos) {
        size_t pos = result.find("Hauser");
        if (pos != std::string::npos) {
            result.replace(pos, 6, "Häuser");
        }
    }
    
    if (result.find("strae") != std::string::npos) {
        size_t pos = result.find("strae");
        if (pos != std::string::npos) {
            result.replace(pos, 5, "straße");
        }
    }
    
    return result;
}

// Process a line of text with German corrections
static std::string correctGermanText(const std::string& text) {
    if (text.empty()) return text;
    
    // First apply basic character corrections
    std::string processed = correctEuropeanCharacters(text);
    
    std::string result;
    std::string currentWord;
    
    for (char c : processed) {
        if (std::isalpha(c) || c == 'ä' || c == 'ö' || c == 'ü' || c == 'ß' ||
            c == 'Ä' || c == 'Ö' || c == 'Ü') {
            currentWord += c;
        } else {
            // Process completed word
            if (!currentWord.empty()) {
                if (looksLikeGermanWord(currentWord)) {
                    result += correctGermanWord(currentWord);
                } else {
                    result += currentWord;
                }
                currentWord.clear();
            }
            result += c;
        }
    }
    
    // Process last word if any
    if (!currentWord.empty()) {
        if (looksLikeGermanWord(currentWord)) {
            result += correctGermanWord(currentWord);
        } else {
            result += currentWord;
        }
    }
    
    return result;
}

#endif // GERMAN_WORD_CORRECTION_H