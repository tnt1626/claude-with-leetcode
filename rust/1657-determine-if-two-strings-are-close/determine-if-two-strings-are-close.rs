impl Solution {
    pub fn close_strings(word1: String, word2: String) -> bool {
        if word1.len() != word2.len() {
            return false;
        }

        let mut f1 = vec![0; 26];
        let mut f2 = vec![0; 26];

        for b in word1.bytes() {
            f1[(b - b'a') as usize] += 1;
        }
        for b in word2.bytes() {
            f2[(b - b'a') as usize] += 1;
        }

        for i in 0..26 {
            if (f1[i] == 0) != (f2[i] == 0) {
                return false;
            }
        }

        let mut s1 = f1.clone();
        let mut s2 = f2.clone();
        s1.sort();
        s2.sort();

        s1 == s2
    }
}