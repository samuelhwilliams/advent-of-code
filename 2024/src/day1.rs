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
    let mut input = input.clone();

    // Unstable sort uses a typically-faster implementation, if the order of equal elements doesn't
    // need to be preserved.
    input.0.sort_unstable();
    input.1.sort_unstable();

    input
        .0
        .iter()
        .zip(input.1.iter())
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
        .map(|el| (el * list2_counts.get(el).unwrap_or(&0)))
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generator() {
        let input = "\
1   5
2   4
3   3
4   2
5   1"
            .trim();

        assert_eq!(
            build_lists(input),
            (vec![1, 2, 3, 4, 5], vec![5, 4, 3, 2, 1])
        );
    }

    #[test]
    fn test_solve_part1() {
        assert_eq!(solve_part1(&(vec![1, 5], vec![3, 6])), 3);
    }

    #[test]
    fn test_solve_part2() {
        assert_eq!(solve_part2(&(vec![1, 5], vec![3, 6])), 0);
        assert_eq!(solve_part2(&(vec![1], vec![1])), 1);
        assert_eq!(solve_part2(&(vec![2], vec![2])), 2);
        assert_eq!(solve_part2(&(vec![2], vec![2, 2])), 4);
    }
}
