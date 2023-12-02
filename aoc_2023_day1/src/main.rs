use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::PathBuf;

use clap::Parser;
use onig::Regex;

const NUMBER_REGEX: &str = "(?=(zero|one|two|three|four|five|six|seven|eight|nine|\\d))";

#[derive(Parser)]
struct Cli {
    file_path: PathBuf,
}

fn parse_matches(string: &str) -> Option<u32> {
    match string {
        "one" => Some(1),
        "two" => Some(2),
        "three" => Some(3),
        "four" => Some(4),
        "five" => Some(5),
        "six" => Some(6),
        "seven" => Some(7),
        "eight" => Some(8),
        "nine" => Some(9),
        _ if { string.len() == 1 } => string.parse::<u32>().ok(),
        _ => None,
    }
}

fn main() {
    let args = Cli::parse();

    let puzzle_input = File::open(&args.file_path).expect("could not open file");
    let puzzle_input_buffer = BufReader::new(&puzzle_input);

    let re = Regex::new(NUMBER_REGEX).unwrap();

    let mut output: u32 = 0;

    for line in puzzle_input_buffer.lines() {
        let filtered_line: Option<Vec<u32>> = match &line {
            Ok(result) => {
                let test = re
                    .captures_iter(result.as_str())
                    .filter_map(|cap| {
                        if !cap.is_empty() {
                            Some(
                                cap.iter_pos()
                                    .filter_map(|pos| pos)
                                    .map(|pos| &result[pos.0..pos.1])
                                    .collect::<Vec<&str>>(),
                            )
                        } else {
                            None
                        }
                    })
                    .flat_map(|caps: Vec<&str>| -> Vec<u32> {
                        caps.iter()
                            .filter_map(|m| parse_matches(m))
                            .collect::<Vec<u32>>()
                    })
                    .collect::<Vec<u32>>();
                Some(test)
            }
            Err(_) => None,
        };

        if let Some(numbers) = filtered_line {
            if numbers.len() == 1 {
                output = output + (numbers[0] * 11);
            } else {
                output = output + (numbers[0] * 10) + numbers[numbers.len() - 1];
            }
        }
    }

    println!("Calibration result: {}", output)
}
