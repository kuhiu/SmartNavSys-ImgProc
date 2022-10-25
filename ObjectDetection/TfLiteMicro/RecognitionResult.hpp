#ifndef __RECOGNITIONRESULT_H__
#define __RECOGNITIONRESULT_H__

#include <cstdint>

struct RecognitionResult {
    /** Score of recognition */
	int8_t recognition_score;
    /** Scorde of no recognition */
	int8_t no_recognition_score;

};

#endif // __RECOGNITIONRESULT_H__