use std::collections::HashMap;

#[aoc_generator(day1)]
pub fn build_lists(input: &str) -> (Vec<u32>, Vec<u32>) {
    input
        .lines()
        .map(|line| {
            let mut lists = line.split_whitespace();
            let list1 = lists.next().unwrap().parse::<u32>().unwrap();
            let list2 = lists.next().unwrap().parse::<u32>().unwrap();
            (list1, list2)
        })
        .unzip()
}

#[aoc(day1, part1)]
pub fn solve_part1(input: &(Vec<u32>, Vec<u32>)) -> u32 {
    let mut sorted_input1 = input.0.clone();
    let mut sorted_input2 = input.1.clone();

    // Unstable sort uses a typically-faster implementation, if the order of equal elements doesn't
    // need to be preserved.
    sorted_input1.sort_unstable();
    sorted_input2.sort_unstable();

    sorted_input1
        .iter()
        .zip(sorted_input2.iter())
        .map(|(&a, &b)| a.abs_diff(b))
        .sum()
}

#[aoc(day1, part2)]
pub fn solve_part2(input: &(Vec<u32>, Vec<u32>)) -> u32 {
    let mut list2_counts = HashMap::new();

    for &el in &input.1 {
        *list2_counts.entry(el).or_insert(0) += 1
    }

    input
        .0
        .iter()
        .map(|&el| (el * list2_counts.get(&el).unwrap_or(&0)))
        .sum()
}
