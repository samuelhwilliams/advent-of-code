use aoc_runner_derive::{aoc, aoc_generator};

#[aoc_generator(day2)]
fn parse(input: &str) -> Vec<Vec<usize>> {
    input
        .lines()
        .map(|line| {
            line.split_whitespace().filter_map(|el| el.parse().ok()).collect()
        })
        .collect()
}

#[aoc(day2, part1)]
fn part1(input: &Vec<Vec<usize>>) -> usize {
    input
        .iter()
        .map(|report| {
            let diffs: Vec<i32> = report
                .windows(2)
                .map(|pair| pair[0] as i32 - pair[1] as i32)
                .collect();

            diffs.iter().all(|&x| x.abs() >= 1 && x.abs() <= 3) && (diffs.iter().all(|&x| x > 0) || diffs.iter().all(|&x| x < 0))
        })
        .filter(|&res| res == true)
        .count()
}

#[aoc(day2, part2)]
fn part2(input: &Vec<Vec<usize>>) -> usize {
    // 503 - TOO LOW
    // 539 - TOO HIGH

    todo! {};
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1_example() {
        assert_eq!(part1(&parse("<EXAMPLE>")), "<RESULT>");
    }

    #[test]
    fn part2_example() {
        assert_eq!(part2(&parse("<EXAMPLE>")), "<RESULT>");
    }
}
