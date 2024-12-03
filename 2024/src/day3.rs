use aoc_runner_derive::aoc;
use regex::Regex;

#[aoc(day3, part1)]
fn part1(input: &str) -> isize {
    let mul_matcher = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();

    input
        .lines()
        .map(|line| {
            mul_matcher
                .captures_iter(line)
                .map(|m| m.extract())
                .map(|(_, [a, b])| (a.parse::<isize>().unwrap(), b.parse::<isize>().unwrap()))
                .collect::<Vec<(isize, isize)>>()
        })
        .flatten()
        .map(|(a, b)| a * b)
        .sum::<isize>()
}

#[aoc(day3, part2)]
fn part2(input: &str) -> String {
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
