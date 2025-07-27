-- 프로젝트 테이블에 새로운 필드들 추가
ALTER TABLE project 
ADD COLUMN time_zone VARCHAR(50) AFTER title,
ADD COLUMN target_months TEXT AFTER time_zone,
ADD COLUMN quarters VARCHAR(100) AFTER target_months;

-- 기존 start_date 컬럼 삭제 (time_zone으로 대체)
ALTER TABLE project DROP COLUMN start_date; 