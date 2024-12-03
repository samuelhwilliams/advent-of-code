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
fn part2(input: &str) -> isize {
    let mut enabled = true;
    let mul_matcher = Regex::new(r"mul\((?P<num1>\d{1,3}),(?P<num2>\d{1,3})\)|(?P<do>do(?:n't)?\(\))").unwrap();

    // // Below solution captures `enabled` into a closure that might live beyond the lifetime of `enabled` =[
    // // I guess back to the old for loops thing. Not very rusty
    // input
    //     .lines()
    //     .flat_map(|line| {
    //         mul_matcher
    //             .captures_iter(line)
    //             .filter_map(|m| {
    //                 if let Some(do_match) = m.name("do") {
    //                     match do_match.as_str() {
    //                         "do" => {
    //                             enabled = true;
    //                             None
    //                         }
    //                         "don't()" => {
    //                             enabled = false;
    //                             None
    //                         }
    //                         _ => panic! {"do or do not. there is no try."},
    //                     }
    //                 } else {
    //                     if enabled == true {
    //                         Some((
    //                             m.name("num1").unwrap().as_str().parse::<isize>().ok()?,
    //                             m.name("num2").unwrap().as_str().parse::<isize>().ok()?
    //                         ))
    //                     } else {
    //                         Some((0, 0))
    //                     }
    //                 }
    //             })
    //     })
    //     .map(|(a, b)| a * b)
    //     .sum::<isize>()

    let mut total = 0;
    for line in input.lines() {
        for m in mul_matcher.captures_iter(line) {
            if let Some(do_match) = m.name("do") {
                match do_match.as_str() {
                    "do()" => enabled = true,
                    "don't()" => enabled = false,
                    _ => panic! {"do or do not. there is no try."},
                }
            } else {
                if enabled == true {
                    let a = m.name("num1").unwrap().as_str().parse::<isize>().unwrap();
                    let b = m.name("num2").unwrap().as_str().parse::<isize>().unwrap();
                    total += a * b;
                }
            }
        }
    }

    total
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
